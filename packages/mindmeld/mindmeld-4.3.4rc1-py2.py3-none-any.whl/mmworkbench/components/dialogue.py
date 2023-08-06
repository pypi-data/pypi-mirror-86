# -*- coding: utf-8 -*-
"""This module contains the dialogue manager component of Workbench"""
import asyncio
from functools import cmp_to_key, partial
import copy
import logging
import random
import json

from .. import path


mod_logger = logging.getLogger(__name__)


class DirectiveNames:
    """A constants object for directive names.

    Attributes:
        LIST (str): A directive to display a list.
        LISTEN (str): A directive to listen (start speech recognition).
        REPLY (str): A directive to display a text view.
        RESET (str): Description
        SPEAK (str): A directive to speak text out loud.
        SUGGESTIONS (str): A view for a list of suggestions.
    """

    LIST = 'list'
    LISTEN = 'listen'
    REPLY = 'reply'
    RESET = 'reset'
    SPEAK = 'speak'
    SUGGESTIONS = 'suggestions'


class DirectiveTypes:
    """A constants object for directive types.

    Attributes:
        ACTION (str): An action directive
        VIEW (str): A view directive.
    """

    VIEW = 'view'
    ACTION = 'action'


class DialogueStateException(Exception):
    def __init__(self, message=None, target_dialogue_state=None):
        super().__init__(message)
        self.target_dialogue_state = target_dialogue_state


class DialogueStateRule:
    """A rule that determines a dialogue state. Each rule represents a pattern that must match in
    order to invoke a particular dialogue state.

    Attributes:
        dialogue_state (str): The name of the dialogue state
        domain (str): The name of the domain to match against
        entity_types (set): The set of entity types to match against
        intent (str): The name of the intent to match against
    """

    logger = mod_logger.getChild('DialogueStateRule')

    def __init__(self, dialogue_state, **kwargs):
        """Initializes a dialogue state rule.

        Args:
            dialogue_state (str): The name of the dialogue state
            domain (str): The name of the domain to match against
            has_entity (str|list|set): A synonym for the ``has_entities`` param
            has_entities (str|list|set): A single entity type or a list of entity types to match
                against.
            intent (str): The name of the intent to match against
        """

        self.dialogue_state = dialogue_state

        key_kwargs = (('domain',), ('intent',), ('has_entity', 'has_entities'),
                      ('targeted_only',), ('default',))
        valid_kwargs = set()
        for keys in key_kwargs:
            valid_kwargs.update(keys)
        for kwarg in kwargs:
            if kwarg not in valid_kwargs:
                raise TypeError(('DialogueStateRule() got an unexpected keyword argument'
                                 ' \'{!s}\'').format(kwarg))

        resolved = {}
        for keys in key_kwargs:
            if len(keys) == 2:
                single, plural = keys
                if single in kwargs and plural in kwargs:
                    msg = 'Only one of {!r} and {!r} can be specified for a dialogue state rule'
                    raise ValueError(msg.format(single, plural, self.__class__.__name__))
                if single in kwargs:
                    resolved[plural] = {kwargs[single]}
                if plural in kwargs:
                    resolved[plural] = set(kwargs[plural])
            elif keys[0] in kwargs:
                resolved[keys[0]] = kwargs[keys[0]]

        self.domain = resolved.get('domain', None)
        self.intent = resolved.get('intent', None)
        self.targeted_only = resolved.get('targeted_only', False)
        self.default = resolved.get('default', False)
        entities = resolved.get('has_entities', None)
        self.entity_types = None
        if entities is not None:
            if isinstance(entities, str):
                # Single entity type passed in
                self.entity_types = frozenset((entities,))
            elif isinstance(entities, (list, set)):
                # List of entity types passed in
                self.entity_types = frozenset(entities)
            else:
                msg = 'Invalid entity specification for dialogue state rule: {!r}'
                raise ValueError(msg.format(entities))

        if self.targeted_only and any([self.domain, self.intent, self.entity_types]):
            raise ValueError('For a dialogue state rule, if targeted_only is '
                             'True, domain, intent, and has_entity must be omitted')

        if self.default and any([self.domain, self.intent, self.entity_types, self.targeted_only]):
            raise ValueError('For a dialogue state rule, if default is True, '
                             'domain, intent, has_entity, and targeted_only must be omitted')

    def apply(self, context):
        """Applies the dialogue state rule to the given context.

        Args:
            context (dict): A request context

        Returns:
            bool: whether or not the context matches
        """
        # Note: this will probably change as the details of "context" are worked out

        # bail if this rule is only reachable via target_dialogue_state
        if self.targeted_only:
            return False

        # check domain is correct
        if self.domain is not None and self.domain != context['domain']:
            return False

        # check intent is correct
        if self.intent is not None and self.intent != context['intent']:
            return False

        # check expected entity types are present
        if self.entity_types is not None:
            # TODO cache entity types
            entity_types = set()
            for entity in context['entities']:
                entity_types.add(entity['type'])

            if len(self.entity_types & entity_types) < len(self.entity_types):
                return False

        return True

    @property
    def complexity(self):
        """Returns an integer representing the complexity of this dialogue state rule.

        Components of a rule in order of increasing complexity are as follows:
            default rule, domains, intents, entity types, entity mappings

        Returns:
            int: A number representing the rule complexity
        """
        complexity = [0] * 4

        if self.entity_types:
            complexity[0] = len(self.entity_types)

        if self.intent:
            complexity[1] = 1

        if self.domain:
            complexity[2] = 1

        if self.default:
            complexity[3] = 1

        return tuple(complexity)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def __repr__(self):
        return '<{} {!r}>'.format(self.__class__.__name__, self.dialogue_state)

    @staticmethod
    def compare(this, that):
        """Compares the complexity of two dialogue state rules

        Args:
            this (DialogueStateRule): a dialogue state rule
            that (DialogueStateRule): a dialogue state rule

        Returns:
            int: the comparison result
                 -1: that is more complex than this
                 0: this and that are equally complex
                 1: this is more complex than that
        """
        if not (isinstance(this, DialogueStateRule) and isinstance(that, DialogueStateRule)):
            return NotImplemented

        # https://docs.python.org/3.0/whatsnew/3.0.html#ordering-comparisons
        return (this.complexity > that.complexity) - (this.complexity < that.complexity)


class DialogueManager:
    logger = mod_logger.getChild('DialogueManager')

    def __init__(self, responder_class=None, async_mode=False):
        self.async_mode = async_mode

        self.handler_map = {}
        self.middlewares = []
        self.rules = []
        self.responder_class = responder_class or DialogueResponder
        self.default_rule = None

    def handle(self, **kwargs):
        """A decorator that is used to register dialogue state rules"""

        def _decorator(func):
            name = kwargs.pop('name', None)
            self.add_dialogue_rule(name, func, **kwargs)
            return func
        return _decorator

    def middleware(self, *args):
        """A decorator that is used to register dialogue handler middleware"""

        def _decorator(func):
            self.add_middleware(func)
            return func

        if args and callable(args[0]):
            # Support syntax: @middleware
            _decorator(args[0])
            return args[0]
        else:
            # Support syntax: @middleware()
            return _decorator

    def add_middleware(self, middleware):
        """Adds middleware for the dialogue manager. Middleware will be
        called for each message before the dialogue state handler. Middleware
        registered first will be called first.

        Args:
            middleware (callable): A dialogue manager middleware
                function
        """
        if self.async_mode and not asyncio.iscoroutinefunction(middleware):
            msg = ('Cannot use middleware {!r} in async mode. '
                   'Middleware must be coroutine function.')
            raise TypeError(msg.format(middleware.__name__))

        self.middlewares.append(middleware)

    def add_dialogue_rule(self, name, handler, **kwargs):
        """Adds a dialogue state rule for the dialogue manager.

        Args:
            name (str): The name of the dialogue state
            handler (function): The dialogue state handler function
            **kwargs (dict): A list of options to be passed to the DialogueStateRule initializer
        """
        if name is None:
            name = handler.__name__

        if self.async_mode and not asyncio.iscoroutinefunction(handler):
            msg = ('Cannot use dialogue state handler {!r} in async mode. '
                   'Handler must be coroutine function in async mode.')
            raise TypeError(msg.format(name))

        rule = DialogueStateRule(name, **kwargs)

        self.rules.append(rule)
        self.rules.sort(key=cmp_to_key(DialogueStateRule.compare), reverse=True)
        if handler is not None:
            old_handler = self.handler_map.get(name)
            if old_handler is not None and old_handler != handler:
                msg = 'Handler mapping is overwriting an existing dialogue state: %s' % name
                raise AssertionError(msg)
            self.handler_map[name] = handler

            if rule.default:
                if self.default_rule:
                    raise AssertionError('Only one default rule may be specified')
                self.default_rule = rule

    def apply_handler(self, context, target_dialogue_state=None):
        """Applies the dialogue state handler for the most complex matching rule

        Args:
            context (dict): The context object from the DM
            target_dialogue_state (str, optional): The target dialogue state
        Returns:
            dict: A dict containing the dialogue state and directives
        """
        if self.async_mode:
            return self._apply_handler_async(context, target_dialogue_state=target_dialogue_state)

        return self._apply_handler_sync(context, target_dialogue_state=target_dialogue_state)

    def _apply_handler_sync(self, context, target_dialogue_state=None):
        """Applies the dialogue state handler for the most complex matching rule

        Args:
            context (dict): The context object from the DM
            target_dialogue_state (str, optional): The target dialogue state
        Returns:
            dict: A dict containing the dialogue state and directives
        """
        for _ in range(3):
            try:
                return self._attempt_handler_sync(
                    context, target_dialogue_state=target_dialogue_state
                )
            except DialogueStateException as e:
                if e.target_dialogue_state and e.target_dialogue_state != target_dialogue_state:
                    target_dialogue_state = e.target_dialogue_state
                else:
                    self.logger.warning(
                        "Ignoring target dialogue state '{}'".format(e.target_dialogue_state)
                    )
                    target_dialogue_state = None

        if target_dialogue_state:
            self.logger.warning(
                "Ignoring target dialogue state '{}'".format(target_dialogue_state)
            )
        return self._attempt_handler_sync(context)

    def _attempt_handler_sync(self, context, target_dialogue_state=None):
        """Tries to apply the dialogue state handler for the most complex matching rule

        Args:
            context (dict): The context object from the DM
            target_dialogue_state (str, optional): The target dialogue state
        Returns:
            dict: A dict containing the dialogue state and directives
        """
        dialogue_state = self._get_dialogue_state(context, target_dialogue_state)
        handler = self._get_dialogue_handler(dialogue_state)
        responder = self._create_responder()
        params = context.get('request', {}).get('params', {})
        language = params.get('language')
        locale = params.get('locale')
        responder.set_locale(language=language, locale=locale)
        res = handler(context, responder)

        if res and 'dialogue_state' in res:
            # Add dialogue flow's sub-dialogue_state if provided
            dialogue_state = '.'.join([dialogue_state, res["dialogue_state"]])
        return {'dialogue_state': dialogue_state, 'directives': responder.directives}

    async def _apply_handler_async(self, context, target_dialogue_state=None):
        """Applies the dialogue state handler for the most complex matching rule

        Args:
            context (dict): The context object from the DM
            target_dialogue_state (str, optional): The target dialogue state
        Returns:
            dict: A dict containing the dialogue state and directives
        """
        for _ in range(3):
            try:
                return await self._attempt_handler_async(
                    context, target_dialogue_state=target_dialogue_state
                )
            except DialogueStateException as e:
                if e.target_dialogue_state != target_dialogue_state:
                    target_dialogue_state = e.target_dialogue_state
                else:
                    self.logger.warning(
                        "Ignoring target dialogue state '{}'".format(e.target_dialogue_state)
                    )
                    target_dialogue_state = None

        if target_dialogue_state:
            self.logger.warning(
                "Ignoring target dialogue state '{}'".format(target_dialogue_state)
            )
        return await self._attempt_handler_async(context)

    async def _attempt_handler_async(self, context, target_dialogue_state=None):
        """Tries to apply the dialogue state handler for the most complex matching rule

        Args:
            context (dict): The context object from the DM
            target_dialogue_state (str, optional): The target dialogue state
        Returns:
            dict: A dict containing the dialogue state and directives
        """
        dialogue_state = self._get_dialogue_state(context, target_dialogue_state)
        handler = self._get_dialogue_handler(dialogue_state)
        responder = self._create_responder()
        params = context.get('request', {}).get('params', {})
        language = params.get('language')
        locale = params.get('locale')
        responder.set_locale(language=language, locale=locale)
        res = await handler(context, responder)
        if res and 'dialogue_state' in res:
            # Add dialogue flow's sub-dialogue_state if provided
            dialogue_state = '.'.join([dialogue_state, res["dialogue_state"]])
        return {'dialogue_state': dialogue_state, 'directives': responder.directives}

    def reprocess(self, target_dialogue_state=None):
        """Forces the dialogue manager to back out of the flow based on the initial target
        dialogue state setting and reselect a handler, following a new target dialogue state

        Args:
            target_dialogue_state (str, optional): a dialogue_state name to push system into
        """
        raise DialogueStateException(
            message="reprocess", target_dialogue_state=target_dialogue_state
        )

    def _get_dialogue_state(self, context, target_dialogue_state=None):
        dialogue_state = None
        for rule in self.rules:
            if target_dialogue_state:
                if target_dialogue_state == rule.dialogue_state:
                    dialogue_state = rule.dialogue_state
                    break
            else:
                if rule.apply(context):
                    dialogue_state = rule.dialogue_state
                    break
        if dialogue_state is None:
            msg = 'Failed to find dialogue state for {domain}.{intent}'.format(
                domain=context.get('domain'), intent=context.get('intent'))
            self.logger.info(msg, context)

        return dialogue_state

    def _get_dialogue_handler(self, dialogue_state):
        handler = self.handler_map[dialogue_state] if dialogue_state else self._default_handler

        for m in reversed(self.middlewares):
            handler = partial(m, handler=handler)

        return handler

    def _create_responder(self):
        return self.responder_class(slots={})

    @staticmethod
    def _default_handler(context, responder):
        # TODO: implement default handler
        pass


class DialogueFlow(DialogueManager):
    """A special dialogue manager subclass used to implement dialogue flows.
    Dialogue flows allow developers to implement multiple turn interactions
    where only a subset of dialogue states should be accessible or where
    different dialogue rules should apply.
    """
    logger = mod_logger.getChild('DialogueFlow')

    all_flows = {}

    def __init__(self, name, entrance_handler, app, **kwargs):
        super().__init__(async_mode=app.async_mode)

        self._name = name

        self.all_flows[name] = self
        self.app = app
        self.exit_flow_states = []

        def _set_target_state(context, responder):
            context.set_target_dialogue_state(self.flow_state)
            return entrance_handler(context, responder)

        async def _async_set_target_state(context, responder):
            context.set_target_dialogue_state(self.flow_state)
            return await entrance_handler(context, responder)

        self._entrance_handler = _async_set_target_state if self.async_mode else _set_target_state
        app.add_dialogue_rule(self.name, self._entrance_handler, **kwargs)
        handler = self._apply_handler_async if self.async_mode else self._apply_handler_sync
        app.add_dialogue_rule(self.flow_state, handler, targeted_only=True)

    @property
    def name(self):
        return self._name

    @property
    def flow_state(self):
        return self._name + '_flow'

    @property
    def dialogue_manager(self):
        if self.app and self.app.app_manager:
            return self.app.app_manager.dialogue_manager
        return None

    def __call__(self, ctx, responder):
        return self._entrance_handler(ctx, responder)

    def use_middleware(self, *args):
        def _decorator(func):
            self.add_middleware(func)
            return func

        try:
            # Support syntax: @middleware
            func = args[0]
            if not callable(func):
                raise TypeError
            _decorator(func)
            return func
        except (IndexError, TypeError):
            # Support syntax: @middleware()
            return _decorator

        self._entrance_handler = func
        return func

    def handle(self, **kwargs):
        def _decorator(func):
            name = kwargs.pop('name', None)
            exit_flow = kwargs.pop('exit_flow', False)
            if exit_flow:
                func_name = name or func.__name__
                self.exit_flow_states.append(func_name)
            self.add_dialogue_rule(name, func, **kwargs)
            return func

        return _decorator

    def _apply_handler_sync(self, context, responder=None):  # pylint: disable=arguments-differ
        """Applies the dialogue state handler for the dialogue flow and set the target dialogue
        state to the flow state

        Args:
            context (DialogueContext)
            responder (DialogueResponder)

        Returns:
            dict: A dict containing the dialogue state and directives
        """
        context.dialogue_flow = self.name
        dialogue_state = self._get_dialogue_state(context)
        handler = self._get_dialogue_handler(dialogue_state)
        if dialogue_state not in self.exit_flow_states:
            context.set_target_dialogue_state(self.flow_state)
        handler(context, responder)

        return {'dialogue_state': dialogue_state, 'directives': responder.directives}

    async def _apply_handler_async(self, context, responder):  # pylint: disable=arguments-differ
        """Applies the dialogue state handler for the dialogue flow and set the target dialogue
        state to the flow state

        Args:
            context (DialogueContext)
            responder (DialogueResponder)

        Returns:
            dict: A dict containing the dialogue state and directives
        """
        context.dialogue_flow = self.name
        dialogue_state = self._get_dialogue_state(context)
        handler = self._get_dialogue_handler(dialogue_state)
        if dialogue_state not in self.exit_flow_states:
            context.set_target_dialogue_state(self.flow_state)
        res = handler(context, responder)
        if asyncio.iscoroutine(res):
            await res

        return {'dialogue_state': dialogue_state, 'directives': responder.directives}

    def _get_dialogue_handler(self, dialogue_state):
        handler = self.handler_map[dialogue_state] if dialogue_state else self._default_handler

        try:
            middlewares = self.middlewares
        except AttributeError:
            middlewares = getattr(self, 'middleware', tuple())

        for m in reversed(middlewares):
            handler = partial(m, handler=handler)

        return handler


class DialogueResponder:
    """The dialogue responder helps generate directives and fill slots in the
    system-generated natural language responses.

    Attributes:
        directives (list): A list of directives that the responder has added
        slots (dict): Values to populate the placeholder slots in the natural language
            response
    """
    logger = mod_logger.getChild('DialogueResponder')
    DirectiveNames = DirectiveNames
    DirectiveTypes = DirectiveTypes

    def __init__(self, slots):
        """Initializes a dialogue responder

        Args:
            slots (dict): Values to populate the placeholder slots in the natural language
                response
        """
        self.slots = slots
        self.directives = []

    def set_locale(self, language=None, locale=None):
        """No-op function to provide logic for the responder once the
        locale and language are known.

        Args:
            language (str): The language code
            locale (str): The locale code
        """
        pass

    def reply(self, text):
        """Adds a 'reply' directive

        Args:
            text (str): The text of the reply
        """
        text = self._process_template(text)
        self.display(DirectiveNames.REPLY, payload={'text': text})

    def speak(self, text):
        """Adds a 'speak' directive

        Args:
            text (str): The text to speak aloud
        """
        text = self._process_template(text)
        self.act(DirectiveNames.SPEAK, payload={'text': text})

    def list(self, items):
        """Adds a 'list' view directive

        Args:
            items (list): The list of dictionary objects
        """
        items = items or []
        self.display(DirectiveNames.LIST, payload=items)

    def suggest(self, suggestions):
        """Adds a 'suggestions' directive

        Args:
            suggestions (list): A list of suggestions
        """
        suggestions = suggestions or []
        self.display(DirectiveNames.SUGGESTIONS, payload=suggestions)

    def listen(self):
        """Adds a 'listen' directive."""
        self.act(DirectiveNames.LISTEN)

    def reset(self):
        """Adds a 'reset' directive."""
        self.act(DirectiveNames.RESET)

    def display(self, name, payload=None):
        """Adds an arbitrary directive of type 'view'.

        Args:
            name (str): The name of the directive
            payload (dict, optional): The payload for the view
        """
        self.direct(name, DirectiveTypes.VIEW, payload=payload)

    def act(self, name, payload=None):
        """Adds an arbitrary directive of type 'action'.

        Args:
            name (str): The name of the directive
            payload (dict, optional): The payload for the action
        """
        self.direct(name, DirectiveTypes.ACTION, payload=payload)

    def direct(self, name, dtype, payload=None):
        """Adds an arbitrary directive

        Args:
            name (str): The name of the directive
            dtype (str): The type of the directive
            payload (dict, optional): The payload for the view
        """

        directive = {'name': name, 'type': dtype}
        if payload:
            directive['payload'] = payload

        self.directives.append(directive)

    def respond(self, directive):
        """Adds an arbitrary directive.

        Args:
            directive (dict): A directive.
        """
        self.logger.warning('respond() is deprecated. Instead use direct().')
        self.directives.append(directive)

    def prompt(self, text):
        """Alias for `reply()`. Deprecated.

        Args:
            text (str): The text of the reply
        """
        self.logger.warning('prompt() is deprecated. '
                            'Please use reply() and listen() instead')
        self.reply(text)

    @staticmethod
    def _choose(items):
        """Chooses a random item from items"""
        if isinstance(items, (tuple, list)):
            return random.choice(items)
        elif isinstance(items, set):
            return random.choice(tuple(items))
        return items

    def _process_template(self, text):
        return self._choose(text).format(**self.slots)


class DialogueContext(dict):
    "A thin wrapper around the dictionary object for our convenience"
    @property
    def dialogue_flow(self):
        return self.get('dialogue_flow', '')

    @dialogue_flow.setter
    def dialogue_flow(self, value):
        self['dialogue_flow'] = value

    def set_target_dialogue_state(self, target_dialogue_state):
        """Set target dialogue state for the next turn

        Args:
             target_dialogue_state (string): Handler name for dialogue state of next turn
        """
        self['params']['target_dialogue_state'] = target_dialogue_state

    def exit_flow(self):
        """Exit the current flow by clearing the target dialogue state"""
        self['params'].pop('target_dialogue_state', None)


class Conversation:
    """The conversation object is a very basic workbench client.

    It can be useful for testing out dialogue flows in python.

    Example:
        >>> convo = Conversation(app_path='path/to/my/app')
        >>> convo.say('Hello')
        ['Hello. I can help you find store hours. How can I help?']
        >>> convo.say('Is the store on elm open?')
        ['The 23 Elm Street Kwik-E-Mart is open from 7:00 to 19:00.']

    Attributes:
        history (list): The history of the conversation. Most recent messages are earliry
        context (dict): The context of the conversation, containing user context
        default_params (dict): The default params to use with each turn. These
            defaults will be overridden by params passed for each turn.
        params (dict): The params returned by the most recent turn.
    """

    logger = mod_logger.getChild('Conversation')

    def __init__(self, app=None, app_path=None, nlp=None, context=None, default_params=None,
                 force_sync=False):
        """
        Args:
            app (Application, optional): An initialized app object. Either app or app_path must
                be given.
            app_path (None, optional): The path to the app data. Used to create an app object.
                Either app or app_path must be given.
            nlp (NaturalLanguageProcessor, optional): A natural language processor for the app.
                If passed, changes to this processor will affect the response from `say()`
            context (dict, optional): The context to be used in the conversation
            default_params (dict, optional): The default params to use with each turn. These
                defaults will be overridden by params passed for each turn.
            force_sync (bool, optional): Force synchronous return for `say()` and `process()`
                even when app is in async mode.
        """
        app = app or path.get_app(app_path)
        app.lazy_init(nlp)
        self._app_manager = app.app_manager
        if not self._app_manager.ready:
            self._app_manager.load()
        self.context = context or {}
        self.history = []
        self.frame = {}
        self.default_params = default_params or {}
        self.force_sync = force_sync
        self.params = {}

    @property
    def session(self):
        raise AttributeError("'session' was removed in Workbench 4.0.0. Use 'context' instead.")

    @session.setter
    def session(self, value):
        raise AttributeError("'session' was removed in Workbench 4.0.0. Use 'context' instead.")

    def say(self, text, params=None, force_sync=False):
        """Send a message in the conversation. The message will be
        processed by the app based on the current state of the conversation and
        returns the extracted messages from the directives.

        Args:
            text (str): The text of a message
            params (dict): The params to use with this message,
                overriding any defaults which may have been set
            force_sync (bool, optional): Force synchronous response
                even when app is in async mode.

        Returns:
            list of str: A text representation of the dialogue responses
        """
        if self._app_manager.async_mode:
            res = self._say_async(text, params=params)
            if self.force_sync or force_sync:
                return asyncio.get_event_loop().run_until_complete(res)
            return res

        response = self.process(text, params=params)

        # handle directives
        response_texts = [self._follow_directive(a) for a in response['directives']]
        return response_texts

    async def _say_async(self, text, params=None):
        """Send a message in the conversation. The message will be
        processed by the app based on the current state of the conversation and
        returns the extracted messages from the directives.

        Args:
            text (str): The text of a message
            params (dict): The params to use with this message,
                overriding any defaults which may have been set
            force_sync (bool, optional): Force synchronous response
                even when app is in async mode.

        Returns:
            list of str: A text representation of the dialogue responses
        """
        response = await self.process(text, params=params)

        # handle directives
        response_texts = [self._follow_directive(a) for a in response['directives']]
        return response_texts

    def process(self, text, params=None, force_sync=False):
        """Send a message in the conversation. The message will be processed by
        the app based on the current state of the conversation and returns
        the response.

        Args:
            text (str): The text of a message
            params (dict): The params to use with this message, overriding any defaults
                which may have been set

        Returns:
            (dictionary): The dictionary Response
        """
        if self._app_manager.async_mode:
            res = self._process_async(text, params=params)
            if self.force_sync or force_sync:
                return asyncio.get_event_loop().run_until_complete(res)
            return res

        if not self._app_manager.ready:
            self._app_manager.load()

        external_params = params or copy.deepcopy(self.default_params)
        params = copy.deepcopy(self.params)
        params.update(external_params)

        response = self._app_manager.parse(text, params=params, context=self.context,
                                           frame=self.frame, history=self.history)

        self.history = response['history']
        self.frame = response['frame']
        self.params = response['params']

        return response

    async def _process_async(self, text, params=None):
        """Send a message in the conversation. The message will be processed by
        the app based on the current state of the conversation and returns
        the response.

        Args:
            text (str): The text of a message
            params (dict): The params to use with this message, overriding any defaults
                which may have been set

        Returns:
            (dictionary): The dictionary Response
        """
        if not self._app_manager.ready:
            await self._app_manager.load()

        external_params = params or copy.deepcopy(self.default_params)
        params = copy.deepcopy(self.params)
        params.update(external_params)

        response = await self._app_manager.parse(text, params=params, context=self.context,
                                                 frame=self.frame, history=self.history)

        self.history = response['history']
        self.frame = response['frame']
        self.params = response['params']

        return response

    def _follow_directive(self, directive):
        msg = ''
        try:
            directive_name = directive['name']
            if directive_name in [DirectiveNames.REPLY, DirectiveNames.SPEAK]:
                msg = directive['payload']['text']
            elif directive_name == DirectiveNames.SUGGESTIONS:
                suggestions = directive['payload']
                if not suggestions:
                    raise ValueError
                msg = 'Suggestion{}:'.format('' if len(suggestions) == 1 else 's')
                texts = []
                for idx, suggestion in enumerate(suggestions):
                    if idx > 0:
                        msg += ', {!r}'
                    else:
                        msg += ' {!r}'

                    texts.append(self._generate_suggestion_text(suggestion))
                msg = msg.format(*texts)
            elif directive_name in DirectiveNames.LIST:
                msg = '\n'.join(
                    [json.dumps(item, indent=4, sort_keys=True) for item in directive['payload']])
            elif directive_name == DirectiveNames.LISTEN:
                msg = 'Listening...'
            elif directive_name == DirectiveNames.RESET:
                msg = 'Resetting...'
        except (KeyError, ValueError, AttributeError):
            msg = "Unsupported response: {!r}".format(directive)

        return msg

    @staticmethod
    def _generate_suggestion_text(suggestion):
        pieces = []
        if 'text' in suggestion:
            pieces.append(suggestion['text'])
        if suggestion['type'] != 'text':
            pieces.append('({})'.format(suggestion['type']))

        return ' '.join(pieces)

    def reset(self):
        self.history = []
        self.frame = {}
        self.params = {}
