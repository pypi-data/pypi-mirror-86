from mondrian import term

import medikit
from medikit.commands.base import Command
from medikit.commands.utils import _read_configuration
from medikit.config.loader import load_feature_extensions
from medikit.events import LoggingDispatcher, ProjectEvent


def write_resources(event):
    pass


class UpdateCommand(Command):
    def add_arguments(self, parser):
        parser.add_argument("--override-requirements", action="store_true")

    @staticmethod
    def handle(config_filename, **kwargs):
        import logging

        logger = logging.getLogger()

        dispatcher = LoggingDispatcher()

        variables, features, files, config = _read_configuration(dispatcher, config_filename)

        # This is a hack, but we'd need a flexible option parser which requires too much work as of today.
        if kwargs.pop("override_requirements", False):
            if "python" in config:
                config["python"].override_requirements = True

        feature_instances = {}
        logger.info(
            "Updating {} with {} features".format(
                term.bold(config.package_name),
                ", ".join(term.bold(term.green(feature_name)) for feature_name in sorted(features)),
            )
        )

        all_features = load_feature_extensions()

        sorted_features = sorted(features)  # sort to have a predictable display order
        for feature_name in sorted_features:
            logger.debug('Initializing feature "{}"...'.format(term.bold(term.green(feature_name))))
            try:
                feature = all_features[feature_name]
            except KeyError as exc:
                logger.exception('Feature "{}" not found.'.format(feature_name))

            if feature:
                feature_instances[feature_name] = feature(dispatcher)

                for req in feature_instances[feature_name].requires:
                    if not req in sorted_features:
                        raise RuntimeError('Unmet dependency: "{}" requires "{}".'.format(feature_name, req))

                for con in feature_instances[feature_name].conflicts:
                    if con in sorted_features:
                        raise RuntimeError(
                            'Conflicting dependency: "{}" conflicts with "{}".'.format(con, feature_name)
                        )
            else:
                raise RuntimeError("Required feature {} not found.".format(feature_name))

        event = ProjectEvent(config=config)
        event.variables, event.files = variables, files

        # todo: add listener dump list in debug/verbose mode ?

        event = dispatcher.dispatch(medikit.on_start, event)

        dispatcher.dispatch(medikit.on_end, event)

        logger.info("Done.")
