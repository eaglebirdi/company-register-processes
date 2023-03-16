from typing import List
from ReasoningVisualization import NamedFile
from ..Configuration import Configuration
from ..IGenerator import IGenerator
from ..GenerationResult import GenerationResult
from ..Helpers.GeneralHelper import is_empty
from .NamingHelper import *

newline = Configuration.newline


class Generator(IGenerator):
    """
    Logic for creating the case-related axioms for A96: LLC Director Appointment
    """

    def __init__(self, configuration: Configuration):
        super().__init__(configuration)

    def create(self, input_data: dict, root_rule: str) -> GenerationResult:
        self._validate(input_data, __file__)

        axiom_files = [
            NamedFile("instances.ax", self._create_instances_axioms(input_data)),
            NamedFile("casefacts.ax", self._create_casefacts_axioms(input_data))
        ]
        main_object_name = self._get_main_object_name(root_rule)

        result = GenerationResult(axiom_files, main_object_name, root_rule)
        return result

    def _create_instances_axioms(self, input_data: dict) -> str:
        company = input_data['company']
        resolution = input_data['resolution']
        meeting = resolution['meeting']
        application = input_data['application']
        shareholders = company['shareholders']
        directors = company['directors']
        new_director = resolution['new_director']

        result = ""
        result += self.inst_helper.create_instance_declaration(get_cname_company(), "company")
        result += self.inst_helper.create_instance_declaration(get_cname_resolution(), "resolution")
        if meeting['occurred']:
            result += self.inst_helper.create_instance_declaration(get_cname_meeting(), "meeting")
        result += self.inst_helper.create_instance_declaration(get_cname_deed(), "deed")
        result += self.inst_helper.create_instance_declaration(get_cname_voting(), "voting")
        result += self.inst_helper.create_instance_declaration(get_cname_application(), "application")
        result += self.inst_helper.create_instance_declaration(get_cname_assurance(), "assurance")

        persons = self._get_all_persons_cnames(shareholders, directors, new_director)
        for person_cname in persons:
            result += self.inst_helper.create_instance_declaration(person_cname, "person")
        for shareholder in shareholders:
            result += self.inst_helper.create_instance_declaration(get_cname_shareholder(shareholder), "shareholder")
        for director in directors:
            result += self.inst_helper.create_instance_declaration(get_cname_director(director), "director")
        result += self.inst_helper.create_instance_declaration(get_cname_director(new_director), "director")

        result += newline
        result += self.inst_helper.create_inequality_constraints(persons)
        result += newline
        shareholders_names = [get_cname_shareholder(x) for x in shareholders]
        result += self.inst_helper.create_inequality_constraints(shareholders_names)
        result += newline
        directors_names = [get_cname_director(x) for x in directors]
        result += self.inst_helper.create_inequality_constraints(directors_names)
        result += newline

        result += self.inst_helper.create_relation_declaration("resolution_newdirector", "resolution", "director", get_cname_resolution(), get_cname_director(new_director))
        result += self.inst_helper.create_relation_declaration("application_resolution", "application", "resolution", get_cname_application(), get_cname_resolution())
        result += self.inst_helper.create_relation_declaration("company_resolution", "company", "resolution", get_cname_company(), get_cname_resolution())

        if meeting['occurred']:
            result += self.inst_helper.create_relation_declaration("resolution_meeting", "resolution", "meeting", get_cname_resolution(), get_cname_meeting())

        result += self.inst_helper.create_relation_declaration("resolution_deed", "resolution", "deed", get_cname_resolution(), get_cname_deed())
        result += self.inst_helper.create_relation_declaration("resolution_voting", "resolution", "voting", get_cname_resolution(), get_cname_voting())
        result += self.inst_helper.create_relation_declaration("application_assurance", "application", "assurance", get_cname_application(), get_cname_assurance())

        return result

    def _create_casefacts_axioms(self, input_data: dict) -> str:
        company = input_data['company']
        resolution = input_data['resolution']
        meeting = resolution['meeting']
        application = input_data['application']
        shareholders = company['shareholders']
        company_directors = company['directors']
        new_director = resolution['new_director']

        cname_company = get_cname_company()
        cname_resolution = get_cname_resolution()

        result = ""

        result += self.fact_helper.create_casefact_declaration_binary("company_representationpower", "company", "representationpower", [(cname_company, company['representationpower'])])

        majorityrequirement = company.get('majorityrequirement')
        if not self.configuration.precompute_arithmetics:
            if majorityrequirement is None:
                company_majreqs = []
            else:
                company_majreqs = [(cname_company, str(majorityrequirement))]
            result += self.fact_helper.create_casefact_declaration_binary("company_majorityrequirement_AoA", "company", "$real", company_majreqs)

        result += newline

        result += self.fact_helper.create_casefact_declaration_binary("shareholder_company", "shareholder", "company", [(get_cname_shareholder(x), cname_company) for x in shareholders])
        result += self.fact_helper.create_casefact_declaration_binary("shareholder_person", "shareholder", "person", [(get_cname_shareholder(x), get_cname_person(x)) for x in shareholders])

        if not self.configuration.precompute_arithmetics:
            result += self.fact_helper.create_casefact_declaration_binary("shareholder_votes", "shareholder", "$int", [(get_cname_shareholder(x), str(x['votes'])) for x in shareholders])

        result += newline

        directors_incl_new = company_directors + [new_director]
        result += self.fact_helper.create_casefact_declaration_binary("director_company", "director", "company", [(get_cname_director(x), cname_company) for x in company_directors])
        result += self.fact_helper.create_casefact_declaration_binary("director_person", "director", "person", [(get_cname_director(x), get_cname_person(x)) for x in directors_incl_new])
        result += self.fact_helper.create_casefact_declaration_binary("director_representationpower", "director", "representationpower", [(get_cname_director(x), x['representationpower']) for x in directors_incl_new if not is_empty(x.get('representationpower'))])
        result += self.fact_helper.create_casefact_declaration_monadic("director_exemption181", "director", [get_cname_director(x) for x in directors_incl_new if x.get('exemption181')])

        if meeting['occurred'] and not is_empty(meeting['format']):
            meeting_formats = [(get_cname_meeting(), meeting['format'])]
        else:
            meeting_formats = []
        result += self.fact_helper.create_casefact_declaration_binary("meeting_format", "meeting", "meetingformat", meeting_formats)

        result += newline

        voting = resolution.get('voting')

        if voting is not None:
            yes_votes = voting.get('yes_votes')
            no_votes = voting.get('no_votes')
            abstentions = voting.get('abstentions')
    
            cname_voting = get_cname_voting()

            if self.configuration.precompute_arithmetics:
                result += self._create_precomputed_majority_axiom(yes_votes, no_votes, majorityrequirement)
            else:
                if yes_votes is not None:
                    result += self.fact_helper.create_casefact_declaration_binary("voting_yesvotes", "voting", "$int", [(cname_voting, str(yes_votes))])
                if no_votes is not None:
                    result += self.fact_helper.create_casefact_declaration_binary("voting_novotes", "voting", "$int", [(cname_voting, str(no_votes))])
                if abstentions is not None:
                    result += self.fact_helper.create_casefact_declaration_binary("voting_abstentions", "voting", "$int", [(cname_voting, str(abstentions))])

            result += newline

        consents_to_teleconference = meeting.get('consents_to_teleconference')
        if consents_to_teleconference is None:
            consents_to_teleconference = []
        result += self.fact_helper.create_casefact_declaration_binary("does_shareholder_consent_to_teleconference_meeting", "meeting", "shareholder", [(get_cname_meeting(), get_cname_shareholder(x)) for x in consents_to_teleconference])

        written_consents = resolution.get('written_consents')
        if written_consents is None:
            written_consents = []
        result += self.fact_helper.create_casefact_declaration_binary("does_shareholder_consent_to_the_determination", "resolution", "shareholder", [(cname_resolution, get_cname_shareholder(x)) for x in written_consents])

        consents_to_voting_in_writing = resolution.get('consents_to_voting_in_writing')
        if consents_to_voting_in_writing is None:
            consents_to_voting_in_writing = []
        result += self.fact_helper.create_casefact_declaration_binary(
            "does_shareholder_consent_to_voting_in_writing", "resolution", "shareholder",
            [(cname_resolution, get_cname_shareholder(x)) for x in consents_to_voting_in_writing])

        result += newline

        if application['assurance_signed']:
            assurance_signers = [(get_cname_assurance(), get_cname_director(new_director))]
        else:
            assurance_signers = []
        result += self.fact_helper.create_casefact_declaration_binary("is_assurance_signed", "assurance", "director", assurance_signers)

        result += self.fact_helper.create_casefact_declaration_binary("deed_format", "deed", "deedformat", [(get_cname_deed(), application['deed_format'])])

        applicants = application.get('applicants')
        result += self.fact_helper.create_casefact_declaration_binary("application_applicant", "application", "director", [(get_cname_application(), get_cname_director(x)) for x in applicants])

        return result

    def _get_main_object_name(self, root_rule: str) -> str:
        if root_rule == "is_application_legal":
            return get_cname_application()

        raise Exception("no implementation provided for root rule " + root_rule)

    def _create_precomputed_majority_axiom(self, yes_votes: Union[str, None], no_votes: Union[str, None], majorityrequirement: Union[str, None]) -> str:
        if yes_votes is None or no_votes is None:
            raise Exception("Arithmetic precompution cannot be performed due to lack of data.")

        yes_votes_int = int(yes_votes)
        no_votes_int = int(no_votes)

        # ToDo: better extract this from the default rule
        majreq = float(majorityrequirement) if majorityrequirement is not None else 0.5
        yes_ratio = yes_votes_int / (yes_votes_int + no_votes_int)
        is_majority = yes_ratio > majreq

        cname_res = get_cname_resolution()
        result = "% precomputed resolution majority: "
        result += "{:6.4f}".format(yes_ratio) + " > " + "{:6.4f}".format(majreq) + "?" + newline
        result += self.fact_helper.create_nonpredcompl_casefact_monadic("is_resolution_passed_via_voting", cname_res, not is_majority)
        return result

    def _get_all_persons_cnames(self, shareholders, company_directors, new_director) -> List[str]:
        names = []
        names += [get_cname_person(x) for x in shareholders]
        names += [get_cname_person(x) for x in company_directors]
        names += [get_cname_person(new_director)]

        names = list(dict.fromkeys(names))

        return names
