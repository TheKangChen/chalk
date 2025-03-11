from abc import ABC
from dataclasses import dataclass, field
from typing import Literal, Optional


# Virtual Class
@dataclass
class VirtualClassInfo:
    class_name: str
    date: str
    weekday: str
    start_time: str
    end_time: str
    drupal_link: Optional[str] = None
    csv_link: Optional[str] = None
    csv_data: Optional[str] = None
    registration_emails: Optional[list[str]] = None
    # email_created: Optional[bool] = None
    # email_sent: Optional[bool] = None
    # calander_event_created: Optional[bool] = None


# Drupal Form
@dataclass
class FormField(ABC):
    key: str
    value: str


# NOTE: Populate Field
@dataclass
class IgnoreConflictsBox(FormField):
    key: str = "field_program_ignore_conflicts[und][1]"
    value: str = "1"


@dataclass
class ClonedFromOtherField(FormField):
    key: str = "changed"
    value: str = ""


# NOTE: Populate Field
@dataclass
class FormBuildIdField(FormField):
    key: str = "form_build_id"
    value: Optional[str] = ""


# NOTE: Populate Field
@dataclass
class FormTokenField(FormField):
    key: str = "form_token"
    value: Optional[str] = ""


# NOTE: Populate Field
@dataclass
class FormIdField(FormField):
    key: str = "form_id"
    value: Optional[str] = ""


# NOTE: Populate Field
@dataclass
class TitleField(FormField):
    key: str = "title"
    value: Optional[str] = ""


@dataclass
class BodySummaryField(FormField):
    key: str = "body[und][0][summary]"
    value: str = ""


# NOTE: Populate Field
@dataclass
class BodyTextField(FormField):
    key: str = "body[und][0][value]"
    value: Optional[str] = ""


@dataclass
class BodyTextFormatField(FormField):
    key: str = "body[und][0][format]"
    value: str = "4"


@dataclass
class ShowEndDateBox(FormField):
    index: int = 0
    key: str = field(init=False)
    value: str = "1"

    def __post_init__(self) -> None:
        self.key = f"field_group_program_dates[und][{str(self.index)}][field_date_time][und][0][show_todate]"


# NOTE: Populate Field & add date validation
@dataclass
class DateStartMonthField(FormField):
    index: int = 0
    key: str = field(init=False)
    value: str

    def __post_init__(self) -> None:
        self.key = f"field_group_program_dates[und][{str(self.index)}][field_date_time][und][0][value][month]"


# NOTE: Populate Field
@dataclass
class DateStartDayField(FormField):
    index: int = 0
    key: str = field(init=False)
    value: str

    def __post_init__(self) -> None:
        self.key = f"field_group_program_dates[und][{str(self.index)}][field_date_time][und][0][value][day]"


# NOTE: Populate Field
@dataclass
class DateStartYearField(FormField):
    index: int = 0
    key: str = field(init=False)
    value: str

    def __post_init__(self) -> None:
        self.key = f"field_group_program_dates[und][{str(self.index)}][field_date_time][und][0][value][year]"


# NOTE: Populate Field
@dataclass
class DateStartHourField(FormField):
    index: int = 0
    key: str = field(init=False)
    value: str

    def __post_init__(self) -> None:
        self.key = f"field_group_program_dates[und][{str(self.index)}][field_date_time][und][0][value][hour]"


# NOTE: Populate Field
@dataclass
class DateStartMinuteField(FormField):
    index: int = 0
    key: str = field(init=False)
    value: str

    def __post_init__(self) -> None:
        self.key = f"field_group_program_dates[und][{str(self.index)}][field_date_time][und][0][value][minute]"


# NOTE: Populate Field
@dataclass
class DateStartAmPmField(FormField):
    index: int = 0
    key: str = field(init=False)
    value: Literal["am", "pm"]

    def __post_init__(self) -> None:
        self.key = f"field_group_program_dates[und][{str(self.index)}][field_date_time][und][0][value][ampm]"


# NOTE: Populate Field
@dataclass
class DateEndMonthField(FormField):
    index: int = 0
    key: str = field(init=False)
    value: str

    def __post_init__(self) -> None:
        self.key = f"field_group_program_dates[und][{str(self.index)}][field_date_time][und][0][value2][month]"


# NOTE: Populate Field
@dataclass
class DateEndDayField(FormField):
    index: int = 0
    key: str = field(init=False)
    value: str

    def __post_init__(self) -> None:
        self.key = f"field_group_program_dates[und][{str(self.index)}][field_date_time][und][0][value2][day]"


# NOTE: Populate Field
@dataclass
class DateEndYearField(FormField):
    index: int = 0
    key: str = field(init=False)
    value: str

    def __post_init__(self) -> None:
        self.key = f"field_group_program_dates[und][{str(self.index)}][field_date_time][und][0][value2][year]"


# NOTE: Populate Field
@dataclass
class DateEndHourField(FormField):
    index: int = 0
    key: str = field(init=False)
    value: str

    def __post_init__(self) -> None:
        self.key = f"field_group_program_dates[und][{str(self.index)}][field_date_time][und][0][value2][hour]"


# NOTE: Populate Field
@dataclass
class DateEndMinuteField(FormField):
    index: int = 0
    key: str = field(init=False)
    value: str

    def __post_init__(self) -> None:
        self.key = f"field_group_program_dates[und][{str(self.index)}][field_date_time][und][0][value2][minute]"


# NOTE: Populate Field
@dataclass
class DateEndAmPmField(FormField):
    index: int = 0
    key: str = field(init=False)
    value: Literal["am", "pm"]

    def __post_init__(self) -> None:
        self.key = f"field_group_program_dates[und][{str(self.index)}][field_date_time][und][0][value2][ampm]"


# NOTE: Populate Field
@dataclass
class DateStatusField(FormField):
    index: int = 0
    key: str = field(init=False)
    value: Literal["_none", "On Hold", "Postponed", "Canceled", "Ongoing"] = "_none"

    def __post_init__(self) -> None:
        self.key = (
            f"field_group_program_dates[und][{str(self.index)}][field_date_status][und]"
        )


@dataclass
class DateDetailsField(FormField):
    index: int = 0
    key: str = field(init=False)
    value: Literal["_none", "On Hold", "Postponed", "Canceled", "Ongoing"] = "_none"

    def __post_init__(self) -> None:
        self.key = f"field_group_program_dates[und][{str(self.index)}][field_date_details][und][0][value]"


# NOTE: Update after class
@dataclass
class DateTotalAdults(FormField):
    index: int = 0
    key: str = field(init=False)
    value: Optional[int | str] = ""

    def __post_init__(self) -> None:
        self.key = f"field_group_program_dates[und][{str(self.index)}][field_total_adults][und][0][value]"
        self.key = str(self.key)


@dataclass
class DateTotalYoungAdults(FormField):
    index: int = 0
    key: str = field(init=False)
    value: Optional[int | str] = ""

    def __post_init__(self) -> None:
        self.key = f"field_group_program_dates[und][{str(self.index)}][field_total_young_adults][und][0][value]"
        self.key = str(self.key)


@dataclass
class DateTotalChildren(FormField):
    index: int = 0
    key: str = field(init=False)
    value: Optional[int | str] = ""

    def __post_init__(self) -> None:
        self.key = f"field_group_program_dates[und][{str(self.index)}][field_total_children][und][0][value]"
        self.key = str(self.key)


@dataclass
class DateWeightHidden(FormField):
    index: int = 0
    key: str = field(init=False)
    value: str = "0"

    def __post_init__(self) -> None:
        self.key = f"field_group_program_dates[und][{str(self.index)}][_weight]"


# NOTE: Populate Field
@dataclass
class LocationField(FormField):
    index: int = 0
    key: str = field(init=False)
    value: int | Literal["_none"]

    def __post_init__(self) -> None:
        self.key = (
            f"field_group_program_location[und][{str(self.index)}][field_location][und]"
        )


# NOTE: Populate Field
@dataclass
class ExternalLocationField(FormField):
    index: int = 0
    key: str = field(init=False)
    value: Optional[str] = ""

    def __post_init__(self) -> None:
        self.key = f"field_group_program_location[und][{str(self.index)}][field_external_location][und][0][value]"


@dataclass
class LocationWeightHidden(FormField):
    index: int = 0
    key: str = field(init=False)
    value: str = "0"

    def __post_init__(self) -> None:
        self.key = f"field_group_program_location[und][{str(self.index)}][_weight]"


@dataclass
class RepeatFreqField(FormField):
    key: str = "nypl_events_repeat[FREQ]"
    value: Literal["DAILY", "WEEKLY", "MONTHLY", "YEARLY"] = "WEEKLY"


@dataclass
class RepeatDailyRadio(FormField):
    key: str = "nypl_events_repeat[daily][byday_radios]"
    value: Literal["INTERVAL", "every_weekday", "every_mo_we_fr", "every_tu_th"] = (
        "INTERVAL"
    )


@dataclass
class RepeatDailyIntervalField(FormField):
    key: str = "nypl_events_repeat[daily][INTERVAL_child]"
    value: int | str = "1"

    def __post_init__(self) -> None:
        self.value = str(self.value)


@dataclass
class RepeatWeeklyIntervalField(FormField):
    key: str = "nypl_events_repeat[weekly][INTERVAL]"
    value: int | str = "1"

    def __post_init__(self) -> None:
        self.value = str(self.value)


@dataclass
class RepeatMonthlyRadio(FormField):
    key: str = "nypl_events_repeat[monthly][day_month]"
    value: Literal["BYMONTHDAY_BYMONTH", "BYDAY_BYMONTH"] = "BYMONTHDAY_BYMONTH"


@dataclass
class RepeatMonthlyOnDayField(FormField):
    key: str = "nypl_events_repeat[monthly][BYMONTHDAY_BYMONTH_child][BYMONTHDAY]"
    value: int | str = "1"

    def __post_init__(self) -> None:
        self.value = str(self.value)


@dataclass
class RepeatMonthlyByDayCountField(FormField):
    key: str = "nypl_events_repeat[monthly][BYDAY_BYMONTH_child][BYDAY_COUNT]"
    value: Literal["+1", "+2", "+3", "+4", "+5", "-1", "-2", "-3", "-4", "-5"] = "+1"


@dataclass
class RepeatMonthlyByWeekdayField(FormField):
    key: str = "nypl_events_repeat[monthly][BYDAY_BYMONTH_child][BYDAY_DAY]"
    value: Literal["SU", "MO", "TU", "WE", "TH", "FR", "SA"] = "SU"


@dataclass
class RepeatYearlyIntervalField(FormField):
    key: str = "nypl_events_repeat[yearly][INTERVAL]"
    value: int | str = "1"

    def __post_init__(self) -> None:
        self.value = str(self.value)


@dataclass
class RepeatYearlyRadio(FormField):
    key: str = "nypl_events_repeat[yearly][day_month]"
    value: Literal["BYMONTHDAY_BYMONTH", "BYDAY_BYMONTH"] = "BYMONTHDAY_BYMONTH"


@dataclass
class RepeatYearlyOnDayField(FormField):
    key: str = "nypl_events_repeat[yearly][BYMONTHDAY_BYMONTH_child][BYMONTHDAY]"
    value: int | str = "1"

    def __post_init__(self) -> None:
        if isinstance(self.value, int):
            if not 1 <= self.value <= 31 and not -31 <= self.value <= -1:
                raise ValueError("Value need to be valid day of month")
        self.value = str(self.value)


@dataclass
class RepeatYearlyByDayCountField(FormField):
    key: str = "nypl_events_repeat[yearly][BYDAY_BYMONTH_child][BYDAY_COUNT]"
    value: Literal["+1", "+2", "+3", "+4", "+5", "-1", "-2", "-3", "-4", "-5"] = "+1"


@dataclass
class RepeatYearlyByWeekdayField(FormField):
    key: str = "nypl_events_repeat[yearly][BYDAY_BYMONTH_child][BYDAY_DAY]"
    value: Literal["SU", "MO", "TU", "WE", "TH", "FR", "SA"] = "SU"


@dataclass
class RepeatStopRepeatRadio(FormField):
    key: str = "nypl_events_repeat[range_of_repeat]"
    value: Literal["COUNT", "UNTIL"] = "COUNT"


@dataclass
class RepeatAfterNField(FormField):
    key: str = "nypl_events_repeat[count_child]"
    value: str = ""


@dataclass
class RepeatUntilDateField(FormField):
    key: str = "nypl_events_repeat[until_child][datetime][date]"
    value: str = ""


@dataclass
class RepeatUntilDateTzHidden(FormField):
    key: str = "nypl_events_repeat[until_child][tz]"
    value: str = ""


@dataclass
class RepeatUntilDateAllDayHidden(FormField):
    key: str = "nypl_events_repeat[until_child][all_day]"
    value: Literal[1, 0, "1", "0"] = "1"

    def __post_init__(self) -> None:
        if self.value == 1:
            self.value = "1"
        if self.value == 0:
            self.value = "0"


@dataclass
class RepeatUntilDateGranularityHidden(FormField):
    key: str = "nypl_events_repeat[until_child][granularity]"
    value: str = 'a:3:{i:0;s:4:"year";i:1;s:5:"month";i:2;s:3:"day";}'


@dataclass
class RepeatExceptionsDateHidden(FormField):
    key: str = "nypl_events_repeat[exceptions][EXDATE][0][datetime][date]"
    value: str = ""


@dataclass
class RepeatExceptionsTzHidden(FormField):
    key: str = "nypl_events_repeat[exceptions][EXDATE][0][tz]"
    value: str = ""


@dataclass
class RepeatExceptionsAllDayHidden(FormField):
    key: str = "nypl_events_repeat[exceptions][EXDATE][0][all_day]"
    value: str = "1"


@dataclass
class RepeatExceptionsGranularityHidden(FormField):
    key: str = "nypl_events_repeat[exceptions][EXDATE][0][granularity]"
    value: str = 'a:3:{i:0;s:4:"year";i:1;s:5:"month";i:2;s:3:"day";}'


@dataclass
class RepeatAdditionsDateHidden(FormField):
    key: str = "nypl_events_repeat[additions][RDATE][0][datetime][date]"
    value: str = ""


@dataclass
class RepeatAdditionsTzHidden(FormField):
    key: str = "nypl_events_repeat[additions][RDATE][0][tz]"
    value: str = ""


@dataclass
class RepeatAdditionsAllDayHidden(FormField):
    key: str = "nypl_events_repeat[additions][RDATE][0][all_day]"
    value: str = "1"


@dataclass
class RepeatAdditionsGranularityHidden(FormField):
    key: str = "nypl_events_repeat[additions][RDATE][0][granularity]"
    value: str = 'a:3:{i:0;s:4:"year";i:1;s:5:"month";i:2;s:3:"day";}'


# NOTE: Populate Field
@dataclass
class EventTypeSelection(FormField):
    key: str = "field_event_type[und]"
    value: int | str = "4315"  # Classes/Workshops

    def __post_init__(self) -> None:
        self.value = str(self.value)


# NOTE: Populate Field
@dataclass
class EventTopicSelection(FormField):
    key: str = "field_event_topic[und]"
    value: int | str = "4261"  # Computers & Technology

    def __post_init__(self) -> None:
        self.value = str(self.value)


# NOTE: Populate Field
@dataclass
class TargetAudienceRadio(FormField):
    key: str = "field_target_audience[und]"
    value: Literal["Adult", "Young Adult", "Children"] = "Adult"


# NOTE: Populate Field
@dataclass
class EventAudienceSelection(FormField):
    key: str = "field_event_audience[und][]"
    value: int | str = "4332"  # Adults

    def __post_init__(self) -> None:
        self.value = str(self.value)


# NOTE: Populate Field
@dataclass
class SeriesSelection(FormField):
    key: str = "field_series[und][]"
    value: int | str = "200787"  # TechConnect

    def __post_init__(self) -> None:
        self.value = str(self.value)


@dataclass
class ExhibitionsField(FormField):
    key: str = "field_exhibitions[und][0][nid]"
    value: str = ""


@dataclass
class ExhibitionsWeightHidden(FormField):
    key: str = "field_exhibitions[und][0][_weight]"
    value: str = "0"

    def __post_init__(self) -> None:
        self.value = str(self.value)


@dataclass
class GrantFunderField(FormField):
    key: str = "field_grant_funder[und][0][value]"
    value: str = ""


@dataclass
class SponsorField(FormField):
    key: str = "field_sponsor[und][0][value]"
    value: str = ""


@dataclass
class RequireTicketSelection(FormField):
    key: str = "field_tickets_required[und]"
    value: Literal["_none", "1", "0"] = "_none"


@dataclass
class TicketCostField(FormField):
    key: str = "field_cost[und][0][value]"
    value: str = ""


@dataclass
class TicketDetailsField(FormField):
    key: str = "field_ticket_details[und][0][value]"
    value: str = ""


@dataclass
class TicketLinkTitleField(FormField):
    key: str = "field_ticket_link[und][0][title]"
    value: str = ""


@dataclass
class TicketLinkUrlField(FormField):
    key: str = "field_ticket_link[und][0][url]"
    value: str = ""


# NOTE: Populate Field
@dataclass
class RegistrationMethodSelection(FormField):
    key: str = "field_signup_method[und]"
    value: int | str | Literal["_none"] = "_none"

    def __post_init__(self) -> None:
        self.value = str(self.value)


@dataclass
class RegistrationDetailsField(FormField):
    key: str = "field_registration_details[und][0][value]"
    value: str = ""


# NOTE: Populate Field
@dataclass
class MaxClassSizeField(FormField):
    key: str = "field_max_class_size[und][0][value]"
    value: int | str = "20"

    def __post_init__(self) -> None:
        self.value = str(self.value)


# NOTE: Auto populate & validate registration date - mm/dd/yyyy
# Should be 1 week before class date (if registration method is not none)
@dataclass
class RegistrationOpenDateField(FormField):
    key: str = "field_signup_open[und][0][value][date]"
    value: str = ""


# NOTE: Auto populate & validate registration time - HH:MM(am/pm)
# Minutes can only be 00 or 30
@dataclass
class RegistrationOpenTimeField(FormField):
    key: str = "field_signup_open[und][0][value][time]"
    value: str = "12:00am"


@dataclass
class SkillPrerequisitesField(FormField):
    key: str = "field_skill_prerequisites[und][0][value]"
    value: str = ""


@dataclass
class ClassFormatSelection(FormField):
    key: str = "field_class_format[und]"
    value: Literal["_none", "Hands on", "Lecture/demonstration"] = "_none"


@dataclass
class ProgramImageChooseFile(FormField):
    key: str = "files[field_program_image_und_0]"
    value: tuple = ("", "", "application/octet-stream")


@dataclass
class ProgramImageWeightHidden(FormField):
    key: str = "field_program_image[und][0][_weight]"
    value: str = "0"


@dataclass
class ProgramImageFidHidden(FormField):
    key: str = "field_program_image[und][0][fid]"
    value: str = "0"


@dataclass
class ProgramImageDisplayHidden(FormField):
    key: str = "field_program_image[und][0][display]"
    value: str = "1"


@dataclass
class ImageGalleryField(FormField):
    key: str = "field_image_gallery_include[und][0][nid]"
    value: str = ""


@dataclass
class ProgramTranscriptChooseFile(FormField):
    key: str = "files[field_program_transcript_und_0]"
    value: tuple = ("", "", "application/octet-stream")


@dataclass
class ProgramTranscriptFidHidden(FormField):
    key: str = "field_program_transcript[und][0][fid]"
    value: str = "0"


@dataclass
class ProgramTranscriptDisplayHidden(FormField):
    key: str = "field_program_transcript[und][0][display]"
    value: str = "1"


@dataclass
class FlyerChooseFile(FormField):
    key: str = "files[field_flyer_und_0]"
    value: tuple = ("", "", "application/octet-stream")


@dataclass
class FlyerFidHidden(FormField):
    key: str = "field_flyer[und][0][fid]"
    value: str = "0"


@dataclass
class FlyerDisplayHidden(FormField):
    key: str = "field_flyer[und][0][display]"
    value: str = "1"


@dataclass
class RelatedPublications(FormField):
    key: str = "field_related_pubs[und][0][nid]"
    value: str = ""


@dataclass
class RelatedPublicationsWeightHidden(FormField):
    key: str = "field_related_pubs[und][0][_weight]"
    value: str = "0"


@dataclass
class TeacherFirstNameField(FormField):
    key: str = "field_teacher_first_name[und][0][value]"
    value: str = ""


@dataclass
class TeacherLastNameField(FormField):
    key: str = "field_teacher_last_name[und][0][value]"
    value: str = ""


@dataclass
class TeacherEmailField(FormField):
    key: str = "field_teacher_email[und][0][email]"
    value: str = ""


@dataclass
class SchoolNameField(FormField):
    key: str = "field_doe_school[und]"
    value: str = ""


@dataclass
class TeacherPhoneNumberField(FormField):
    key: str = "field_teacher_phone_number[und][0][value]"
    value: str = ""


@dataclass
class SchoolTypeSelection(FormField):
    key: str = "field_school_type[und]"
    value: Literal[
        "_none",
        "Public",
        "Private",
        "Parochial",
        "Daycare Center",
        "Home School",
        "Charter",
    ] = "_none"


@dataclass
class GradeAgeSelection(FormField):
    key: str = "field_grade_age[und]"
    value: int | str | Literal["_none"] = "_none"

    def __post_init__(self) -> None:
        if isinstance(self.value, int) and not 1 <= self.value <= 24:
            raise ValueError("Value needs to be integer between 1 and 24")
        self.value = str(self.value)


@dataclass
class OutreachActivityTypeSelection(FormField):
    key: str = "field_doe_outreach_activities[und]"
    value: Literal[
        "_none",
        "General information",
        "Activating student cards",
        "Teacher sets",
        "Union catalog",
        "NYPL e-resources",
        "Branch promotion",
    ] = "_none"


@dataclass
class CommentsField(FormField):
    key: str = "field_comments[und][0][value]"
    value: str = ""


@dataclass
class EventCapacityField(FormField):
    key: str = "field_event_capacity[und][0][value]"
    value: str = ""


@dataclass
class ProgramContentField(FormField):
    key: str = "field_materials_used[und][0][value]"
    value: str = ""


@dataclass
class PreparationTimeField(FormField):
    key: str = "field_preparation_totat_time[und][0][value]"
    value: str = ""


@dataclass
class EventTotalTimeField(FormField):
    key: str = "field_event_total_time[und][0][value]"
    value: str = ""


@dataclass
class AccessibilityServicesNoteBox(FormField):
    key: str = "field_access_services_note[und]"
    value: str = "1"


# NOTE: Populate Field
@dataclass
class PersonField(FormField):
    key: str = "field_person[und][0][value]"
    value: str = ""


# NOTE: Populate Field
@dataclass
class PersonTypeField(FormField):
    key: str = "field_person_type[und]"
    value: int | str = "936"  # Instructor

    def __post_init__(self):
        self.value = str(self.value)


@dataclass
class ShowOnHomePageBox(FormField):
    key: str = "field_featured_event_homepage[und]"
    value: str = "1"


@dataclass
class FeatureEventDateStartMonthField(FormField):
    key: str = "field_featured_event_date[und][0][value][month]"
    value: str = ""


@dataclass
class FeatureEventDateStartDayField(FormField):
    key: str = "field_featured_event_date[und][0][value][day]"
    value: str = ""


@dataclass
class FeatureEventDateStartYearField(FormField):
    key: str = "field_featured_event_date[und][0][value][year]"
    value: str = ""


@dataclass
class FeatureEventDateStartHourField(FormField):
    key: str = "field_featured_event_date[und][0][value][hour]"
    value: str = ""


@dataclass
class FeatureEventDateStartMinuteField(FormField):
    key: str = "field_featured_event_date[und][0][value][minute]"
    value: str = ""


@dataclass
class FeatureEventDateStartAmPmField(FormField):
    key: str = "field_featured_event_date[und][0][value][ampm]"
    value: str = ""


@dataclass
class FeatureEventDateEndMonthField(FormField):
    key: str = "field_featured_event_date[und][0][value2][month]"
    value: str = ""


@dataclass
class FeatureEventDateEndDayField(FormField):
    key: str = "field_featured_event_date[und][0][value2][day]"
    value: str = ""


@dataclass
class FeatureEventDateEndYearField(FormField):
    key: str = "field_featured_event_date[und][0][value2][year]"
    value: str = ""


@dataclass
class FeatureEventDateEndHourField(FormField):
    key: str = "field_featured_event_date[und][0][value2][hour]"
    value: str = ""


@dataclass
class FeatureEventDateEndMinuteField(FormField):
    key: str = "field_featured_event_date[und][0][value2][minute]"
    value: str = ""


@dataclass
class FeatureEventDateEndAmPmField(FormField):
    key: str = "field_featured_event_date[und][0][value2][ampm]"
    value: str = ""


@dataclass
class WorkflowDisclaimerField(FormField):
    key: str = "field_workflow_disclaimer[und][0][value]"
    value: str = ""


@dataclass
class SaveFormButton(FormField):
    key: str = "op"
    value: Literal["Save", "Preview"] = "Save"


DRUPAL_EVENT_MENU_SETTINGS = {
    "menu[link_title]": (None, ""),
    "menu[description]": (None, ""),
    "menu[parent]": (None, "main-menu:0"),
    "menu[weight]": (None, "0"),
}


DRUPAL_EVENT_REVISION_INFO = {
    "log": (None, ""),
}


DRUPAL_EVENT_PATH_SETTINGS = {
    "path[alias]": (None, ""),
}


DRUPAL_EVENT_COMMENT_SETTINGS = {
    "comment": (None, "1"),  # Values: {"Closed": "1", "Open": "2"}
}


DRUPAL_EVENT_ADDITIONAL_SETTINGS = {
    "additional_settings__active_tab": (None, "edit-menu"),  # Values: "edit-revision-information", "edit-path", "edit-metatags", "edit-comment-settings"
}


DRUPAL_EVENT_META_TAGS = {
    "metatags[und][title][value]": (None, "[node:title] | [site:name]"),
    "metatags[und][title][default]": (None, "[node:title] | [site:name]"),
    "metatags[und][description][value]": (None, "[node:summary]"),
    "metatags[und][description][default]": (None, "[node:summary]"),
    "metatags[und][abstract][value]": (None, ""),
    "metatags[und][abstract][default]": (None, ""),
    "metatags[und][keywords][value]": (
        None,
        "NYPL, The New York Public Library, Manhattan, Bronx, Staten Island",
    ),
    "metatags[und][keywords][default]": (
        None,
        "NYPL, The New York Public Library, Manhattan, Bronx, Staten Island",
    ),
    "metatags[und][author][value]": (None, ""),
    "metatags[und][robots][max-snippet]": (None, ""),
    "metatags[und][robots][max-image-preview]": (None, ""),
    "metatags[und][robots][max-video-preview]": (None, ""),
    "metatags[und][robots][default]": (None, ""),
    "metatags[und][news_keywords][value]": (None, ""),
    "metatags[und][news_keywords][default]": (None, ""),
    "metatags[und][standout][value]": (None, ""),
    "metatags[und][standout][default]": (None, ""),
    "metatags[und][rating][value]": (None, ""),
    "metatags[und][rating][default]": (None, ""),
    "metatags[und][referrer][value]": (None, ""),
    "metatags[und][referrer][default]": (None, ""),
    "metatags[und][rights][value]": (
        None,
        "© [current-date:custom:Y] The New York Public Library ",
    ),
    "metatags[und][rights][default]": (
        None,
        "© [current-date:custom:Y] The New York Public Library ",
    ),
    "metatags[und][image_src][value]": (None, ""),
    "metatags[und][image_src][default]": (None, ""),
    "metatags[und][canonical][value]": (None, ""),
    "metatags[und][canonical][default]": (None, ""),
    "metatags[und][set_cookie][value]": (None, ""),
    "metatags[und][shortlink][value]": (None, ""),
    "metatags[und][shortlink][default]": (None, ""),
    "metatags[und][original-source][value]": (None, ""),
    "metatags[und][original-source][default]": (None, ""),
    "metatags[und][prev][value]": (None, ""),
    "metatags[und][prev][default]": (None, ""),
    "metatags[und][next][value]": (None, ""),
    "metatags[und][next][default]": (None, ""),
    "metatags[und][content-language][value]": (None, ""),
    "metatags[und][content-language][default]": (None, ""),
    "metatags[und][geo.position][value]": (None, ""),
    "metatags[und][geo.position][default]": (None, ""),
    "metatags[und][geo.placename][value]": (None, ""),
    "metatags[und][geo.placename][default]": (None, ""),
    "metatags[und][geo.region][value]": (None, ""),
    "metatags[und][geo.region][default]": (None, ""),
    "metatags[und][icbm][value]": (None, ""),
    "metatags[und][icbm][default]": (None, ""),
    "metatags[und][refresh][value]": (None, ""),
    "metatags[und][refresh][default]": (None, ""),
    "metatags[und][revisit-after][value]": (None, ""),
    "metatags[und][revisit-after][period]": (None, ""),
    "metatags[und][revisit-after][default]": (None, ""),
    "metatags[und][pragma][value]": (None, ""),
    "metatags[und][pragma][default]": (None, ""),
    "metatags[und][cache-control][value]": (None, ""),
    "metatags[und][cache-control][default]": (None, ""),
    "metatags[und][expires][value]": (None, ""),
    "metatags[und][expires][default]": (None, ""),
    "metatags[und][google][value]": (None, ""),
    "metatags[und][og:type][value]": (None, ""),
    "metatags[und][og:type][default]": (None, ""),
    "metatags[und][og:url][value]": (None, "[current-page:url:absolute]"),
    "metatags[und][og:url][default]": (None, "[current-page:url:absolute]"),
    "metatags[und][og:title][value]": (None, "[node:title]"),
    "metatags[und][og:title][default]": (None, "[node:title]"),
    "metatags[und][og:determiner][value]": (None, ""),
    "metatags[und][og:determiner][default]": (None, ""),
    "metatags[und][og:description][value]": (None, "[node:summary]"),
    "metatags[und][og:description][default]": (None, "[node:summary]"),
    "metatags[und][og:updated_time][value]": (None, ""),
    "metatags[und][og:updated_time][default]": (None, ""),
    "metatags[und][og:see_also][value]": (None, ""),
    "metatags[und][og:see_also][default]": (None, ""),
    "metatags[und][og:image][value]": (
        None,
        "https://ux-static.nypl.org/images/social-sharing/default+events+img-FINAL_868x455.png",
    ),
    "metatags[und][og:image][default]": (
        None,
        "https://ux-static.nypl.org/images/social-sharing/default+events+img-FINAL_868x455.png",
    ),
    "metatags[und][og:image:url][value]": (None, ""),
    "metatags[und][og:image:url][default]": (None, ""),
    "metatags[und][og:image:secure_url][value]": (None, ""),
    "metatags[und][og:image:secure_url][default]": (None, ""),
    "metatags[und][og:image:alt][value]": (None, ""),
    "metatags[und][og:image:type][value]": (None, "image/png"),
    "metatags[und][og:image:type][default]": (None, "image/png"),
    "metatags[und][og:image:width][value]": (None, "868"),
    "metatags[und][og:image:width][default]": (None, "868"),
    "metatags[und][og:image:height][value]": (None, "455"),
    "metatags[und][og:image:height][default]": (None, "455"),
    "metatags[und][og:latitude][value]": (None, ""),
    "metatags[und][og:latitude][default]": (None, ""),
    "metatags[und][og:longitude][value]": (None, ""),
    "metatags[und][og:longitude][default]": (None, ""),
    "metatags[und][og:street_address][value]": (None, ""),
    "metatags[und][og:street_address][default]": (None, ""),
    "metatags[und][og:locality][value]": (None, ""),
    "metatags[und][og:locality][default]": (None, ""),
    "metatags[und][og:region][value]": (None, ""),
    "metatags[und][og:region][default]": (None, ""),
    "metatags[und][og:postal_code][value]": (None, ""),
    "metatags[und][og:postal_code][default]": (None, ""),
    "metatags[und][og:country_name][value]": (None, ""),
    "metatags[und][og:country_name][default]": (None, ""),
    "metatags[und][og:email][value]": (None, ""),
    "metatags[und][og:email][default]": (None, ""),
    "metatags[und][og:phone_number][value]": (None, ""),
    "metatags[und][og:phone_number][default]": (None, ""),
    "metatags[und][og:fax_number][value]": (None, ""),
    "metatags[und][og:fax_number][default]": (None, ""),
    "metatags[und][og:locale][value]": (None, ""),
    "metatags[und][og:locale][default]": (None, ""),
    "metatags[und][og:locale:alternate][value]": (None, ""),
    "metatags[und][og:locale:alternate][default]": (None, ""),
    "metatags[und][article:author][value]": (None, ""),
    "metatags[und][article:author][default]": (None, ""),
    "metatags[und][article:publisher][value]": (None, ""),
    "metatags[und][article:publisher][default]": (None, ""),
    "metatags[und][article:section][value]": (None, ""),
    "metatags[und][article:section][default]": (None, ""),
    "metatags[und][article:tag][value]": (None, ""),
    "metatags[und][article:tag][default]": (None, ""),
    "metatags[und][article:published_time][value]": (None, ""),
    "metatags[und][article:published_time][default]": (None, ""),
    "metatags[und][article:modified_time][value]": (None, ""),
    "metatags[und][article:modified_time][default]": (None, ""),
    "metatags[und][article:expiration_time][value]": (None, ""),
    "metatags[und][article:expiration_time][default]": (None, ""),
    "metatags[und][profile:first_name][value]": (None, ""),
    "metatags[und][profile:first_name][default]": (None, ""),
    "metatags[und][profile:last_name][value]": (None, ""),
    "metatags[und][profile:last_name][default]": (None, ""),
    "metatags[und][profile:username][value]": (None, ""),
    "metatags[und][profile:username][default]": (None, ""),
    "metatags[und][profile:gender][value]": (None, ""),
    "metatags[und][profile:gender][default]": (None, ""),
    "metatags[und][og:audio][value]": (None, ""),
    "metatags[und][og:audio][default]": (None, ""),
    "metatags[und][og:audio:secure_url][value]": (None, ""),
    "metatags[und][og:audio:secure_url][default]": (None, ""),
    "metatags[und][og:audio:type][value]": (None, ""),
    "metatags[und][og:audio:type][default]": (None, ""),
    "metatags[und][book:author][value]": (None, ""),
    "metatags[und][book:author][default]": (None, ""),
    "metatags[und][book:isbn][value]": (None, ""),
    "metatags[und][book:isbn][default]": (None, ""),
    "metatags[und][book:release_date][value]": (None, ""),
    "metatags[und][book:release_date][default]": (None, ""),
    "metatags[und][book:tag][value]": (None, ""),
    "metatags[und][book:tag][default]": (None, ""),
    "metatags[und][og:video:url][value]": (None, ""),
    "metatags[und][og:video:url][default]": (None, ""),
    "metatags[und][og:video:secure_url][value]": (None, ""),
    "metatags[und][og:video:secure_url][default]": (None, ""),
    "metatags[und][og:video:width][value]": (None, ""),
    "metatags[und][og:video:width][default]": (None, ""),
    "metatags[und][og:video:height][value]": (None, ""),
    "metatags[und][og:video:height][default]": (None, ""),
    "metatags[und][og:video:type][value]": (None, ""),
    "metatags[und][og:video:type][default]": (None, ""),
    "metatags[und][video:actor][value]": (None, ""),
    "metatags[und][video:actor][default]": (None, ""),
    "metatags[und][video:actor:role][value]": (None, ""),
    "metatags[und][video:actor:role][default]": (None, ""),
    "metatags[und][video:director][value]": (None, ""),
    "metatags[und][video:director][default]": (None, ""),
    "metatags[und][video:writer][value]": (None, ""),
    "metatags[und][video:writer][default]": (None, ""),
    "metatags[und][video:duration][value]": (None, ""),
    "metatags[und][video:duration][default]": (None, ""),
    "metatags[und][video:release_date][value]": (None, ""),
    "metatags[und][video:release_date][default]": (None, ""),
    "metatags[und][video:tag][value]": (None, ""),
    "metatags[und][video:tag][default]": (None, ""),
    "metatags[und][video:series][value]": (None, ""),
    "metatags[und][video:series][default]": (None, ""),
    "metatags[und][fb:admins][value]": (None, ""),
    "metatags[und][fb:admins][default]": (None, ""),
    "metatags[und][fb:app_id][value]": (None, ""),
    "metatags[und][fb:app_id][default]": (None, ""),
    "metatags[und][fb:pages][value]": (None, ""),
    "metatags[und][fb:pages][default]": (None, ""),
    "metatags[und][twitter:card][value]": (None, "summary_large_image"),
    "metatags[und][twitter:card][default]": (None, "summary_large_image"),
    "metatags[und][twitter:creator][value]": (None, ""),
    "metatags[und][twitter:creator][default]": (None, ""),
    "metatags[und][twitter:creator:id][value]": (None, ""),
    "metatags[und][twitter:creator:id][default]": (None, ""),
    "metatags[und][twitter:url][value]": (None, ""),
    "metatags[und][twitter:url][default]": (None, ""),
    "metatags[und][twitter:title][value]": (None, ""),
    "metatags[und][twitter:title][default]": (None, ""),
    "metatags[und][twitter:description][value]": (None, ""),
    "metatags[und][twitter:description][default]": (None, ""),
    "metatags[und][twitter:dnt][value]": (None, ""),
    "metatags[und][twitter:image][value]": (
        None,
        "https://ux-static.nypl.org/images/social-sharing/default+events+img-FINAL_868x489.png",
    ),
    "metatags[und][twitter:image][default]": (
        None,
        "https://ux-static.nypl.org/images/social-sharing/default+events+img-FINAL_868x489.png",
    ),
    "metatags[und][twitter:image:width][value]": (None, ""),
    "metatags[und][twitter:image:width][default]": (None, ""),
    "metatags[und][twitter:image:height][value]": (None, ""),
    "metatags[und][twitter:image:height][default]": (None, ""),
    "metatags[und][twitter:image:alt][value]": (None, ""),
    "metatags[und][twitter:image:alt][default]": (None, ""),
    "metatags[und][twitter:image0][value]": (None, ""),
    "metatags[und][twitter:image0][default]": (None, ""),
    "metatags[und][twitter:image1][value]": (None, ""),
    "metatags[und][twitter:image1][default]": (None, ""),
    "metatags[und][twitter:image2][value]": (None, ""),
    "metatags[und][twitter:image2][default]": (None, ""),
    "metatags[und][twitter:image3][value]": (None, ""),
    "metatags[und][twitter:image3][default]": (None, ""),
    "metatags[und][twitter:player][value]": (None, ""),
    "metatags[und][twitter:player][default]": (None, ""),
    "metatags[und][twitter:player:width][value]": (None, ""),
    "metatags[und][twitter:player:width][default]": (None, ""),
    "metatags[und][twitter:player:height][value]": (None, ""),
    "metatags[und][twitter:player:height][default]": (None, ""),
    "metatags[und][twitter:player:stream][value]": (None, ""),
    "metatags[und][twitter:player:stream][default]": (None, ""),
    "metatags[und][twitter:player:stream:content_type][value]": (None, ""),
    "metatags[und][twitter:player:stream:content_type][default]": (None, ""),
    "metatags[und][twitter:app:country][value]": (None, ""),
    "metatags[und][twitter:app:country][default]": (None, ""),
    "metatags[und][twitter:app:name:iphone][value]": (None, ""),
    "metatags[und][twitter:app:name:iphone][default]": (None, ""),
    "metatags[und][twitter:app:id:iphone][value]": (None, ""),
    "metatags[und][twitter:app:id:iphone][default]": (None, ""),
    "metatags[und][twitter:app:url:iphone][value]": (None, ""),
    "metatags[und][twitter:app:url:iphone][default]": (None, ""),
    "metatags[und][twitter:app:name:ipad][value]": (None, ""),
    "metatags[und][twitter:app:name:ipad][default]": (None, ""),
    "metatags[und][twitter:app:id:ipad][value]": (None, ""),
    "metatags[und][twitter:app:id:ipad][default]": (None, ""),
    "metatags[und][twitter:app:url:ipad][value]": (None, ""),
    "metatags[und][twitter:app:url:ipad][default]": (None, ""),
    "metatags[und][twitter:app:name:googleplay][value]": (None, ""),
    "metatags[und][twitter:app:name:googleplay][default]": (None, ""),
    "metatags[und][twitter:app:id:googleplay][value]": (None, ""),
    "metatags[und][twitter:app:id:googleplay][default]": (None, ""),
    "metatags[und][twitter:app:url:googleplay][value]": (None, ""),
    "metatags[und][twitter:app:url:googleplay][default]": (None, ""),
    "metatags[und][twitter:label1][value]": (None, ""),
    "metatags[und][twitter:label1][default]": (None, ""),
    "metatags[und][twitter:data1][value]": (None, ""),
    "metatags[und][twitter:data1][default]": (None, ""),
    "metatags[und][twitter:label2][value]": (None, ""),
    "metatags[und][twitter:label2][default]": (None, ""),
    "metatags[und][twitter:data2][value]": (None, ""),
    "metatags[und][twitter:data2][default]": (None, ""),
}
