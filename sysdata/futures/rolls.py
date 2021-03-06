
from syslogdiag.log import logtoscreen

USE_CHILD_CLASS_ROLL_PARAMS_ERROR = "You need to use a child class of rollParametersData"


class rollParametersMissing(Exception):
    pass

class rollParametersData(object):
    """
    Read and write data class to get roll data for a given instrument

    We'd inherit from this class for a specific implementation

    """

    def __init__(self, log=logtoscreen("futuresInstrumentData")):
        self._log = log

    @property
    def log(self):
        return self._log

    def __repr__(self):
        return "rollParametersData base class - DO NOT USE"

    def keys(self):
        return self.get_list_of_instruments()

    def get_list_of_instruments(self):
        raise NotImplementedError(USE_CHILD_CLASS_ROLL_PARAMS_ERROR)

    def get_roll_parameters(self, instrument_code):
        if self.is_code_in_data(instrument_code):
            return self._get_roll_parameters_without_checking(instrument_code)
        else:
            raise rollParametersMissing("Don't have parameters for %s" % instrument_code)

    def _get_roll_parameters_without_checking(self, instrument_code):
        raise NotImplementedError(USE_CHILD_CLASS_ROLL_PARAMS_ERROR)

    def __getitem__(self, instrument_code):
        return self.get_roll_parameters(instrument_code)

    def delete_roll_parameters(self, instrument_code, are_you_sure=False):
        self.log.label(instrument_code=instrument_code)

        if are_you_sure:
            if self.is_code_in_data(instrument_code):
                self._delete_roll_parameters_data_without_any_warning_be_careful(
                    instrument_code)
                self.log.terse(
                    "Deleted roll parameters for %s" %
                    instrument_code)

            else:
                # doesn't exist anyway
                self.log.warn(
                    "Tried to delete roll parameters for non existent instrument code %s" %
                    instrument_code)
        else:
            self.log.error(
                "You need to call delete_roll_parameters with a flag to be sure"
            )

    def _delete_roll_parameters_data_without_any_warning_be_careful(self,
            instrument_code):
        raise NotImplementedError(USE_CHILD_CLASS_ROLL_PARAMS_ERROR)

    def is_code_in_data(self, instrument_code):
        if instrument_code in self.get_list_of_instruments():
            return True
        else:
            return False

    def add_roll_parameters(
        self, roll_parameters, instrument_code, ignore_duplication=False
    ):

        self.log.label(instrument_code=instrument_code)

        if self.is_code_in_data(instrument_code):
            if ignore_duplication:
                pass
            else:
                raise self.log.warn(
                    "There is already %s in the data, you have to delete it first" %
                    instrument_code)

        self._add_roll_parameters_without_checking_for_existing_entry(
            roll_parameters, instrument_code
        )

        self.log.terse(
            "Added roll parameters for instrument %s" %
            instrument_code)

    def _add_roll_parameters_without_checking_for_existing_entry(
        self, roll_parameters, instrument_code
    ):
        raise NotImplementedError(USE_CHILD_CLASS_ROLL_PARAMS_ERROR)
