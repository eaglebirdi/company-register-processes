from typing import List
from ReasoningVisualization import NamedFile
from ..Configuration import Configuration
from ..IGenerator import IGenerator
from ..GenerationResult import GenerationResult
from ..Helpers.GeneralHelper import is_empty
from .NamingHelper import *

newline = Configuration.newline


class Generator(IGenerator):
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

        result = ""
        result += self.inst_helper.create_instance_declaration(get_cname_company(), "company")
        result += self.inst_helper.create_instance_declaration(get_cname_resolution(), "resolution")
        if meeting['occurred']:
            result += self.inst_helper.create_instance_declaration(get_cname_meeting(), "meeting")
        result += self.inst_helper.create_instance_declaration(get_cname_deed(), "deed")
        result += self.inst_helper.create_instance_declaration(get_cname_voting(), "voting")
        result += self.inst_helper.create_instance_declaration(get_cname_application(), "application")
        result += self.inst_helper.create_instance_declaration(get_cname_assurance(), "assurance")

        directors_and_liquidators = self.get_directors_and_liquidators(input_data)

        company_liquidators = company.get('liquidators')
        if company_liquidators is not None:
            result += self.inst_helper.create_instance_declaration(get_cname_liquidatorlist_AoA(), "liquidatorlist")

        resolution_liquidators = resolution.get('liquidators')
        if resolution_liquidators is not None:
            result += self.inst_helper.create_instance_declaration(get_cname_liquidatorlist_resolution(), "liquidatorlist")

        persons = self.get_all_persons_cnames(shareholders, directors_and_liquidators)
        for person_cname in persons:
            result += self.inst_helper.create_instance_declaration(person_cname, "person")
        for shareholder in shareholders:
            result += self.inst_helper.create_instance_declaration(get_cname_shareholder(shareholder), "shareholder")
        for cname_dirliq, dirliq in directors_and_liquidators:
            result += self.inst_helper.create_instance_declaration(cname_dirliq, "director")

        result += newline
        result += self.inst_helper.create_inequality_constraints(persons)
        result += newline
        shareholders_names = [get_cname_shareholder(x) for x in shareholders]
        result += self.inst_helper.create_inequality_constraints(shareholders_names)
        result += newline
        directors_names = list(dict.fromkeys([x for x, y in directors_and_liquidators]))
        result += self.inst_helper.create_inequality_constraints(directors_names)
        result += newline

        result += self.inst_helper.create_relation_declaration("application_resolution", "application", "resolution", get_cname_application(), get_cname_resolution())
        result += self.inst_helper.create_relation_declaration("company_resolution", "company", "resolution", get_cname_company(), get_cname_resolution())

        if meeting['occurred']:
            result += self.inst_helper.create_relation_declaration("resolution_meeting", "resolution", "meeting", get_cname_resolution(), get_cname_meeting())

        result += self.inst_helper.create_relation_declaration("application_deed", "application", "deed", get_cname_application(), get_cname_deed())
        result += self.inst_helper.create_relation_declaration("resolution_voting", "resolution", "voting", get_cname_resolution(), get_cname_voting())
        result += self.inst_helper.create_relation_declaration("application_assurance", "application", "assurance", get_cname_application(), get_cname_assurance())

        if company_liquidators is not None:
            result += self.inst_helper.create_relation_declaration("company_AoA_liquidatorlist", "company", "liquidatorlist", get_cname_company(), get_cname_liquidatorlist_AoA())

        if resolution_liquidators is not None:
            result += self.inst_helper.create_relation_declaration("resolution_liquidatorlist", "resolution", "liquidatorlist", get_cname_resolution(), get_cname_liquidatorlist_resolution())

        return result

    def _create_casefacts_axioms(self, input_data: dict) -> str:
        company = input_data['company']
        resolution = input_data['resolution']
        meeting = resolution['meeting']
        application = input_data['application']
        shareholders = company['shareholders']
        directors = company['directors']
        assurance_signers = application['assurance_signers']

        cname_company = get_cname_company()
        cname_resolution = get_cname_resolution()

        result = ""

        result += self.fact_helper.create_casefact_declaration_binary("company_representationpower", "company", "representationpower", [(cname_company, company['representationpower'])])

        company_expirations = []
        if company['has_expiration_date']:
            company_expirations += [get_cname_company()]
        result += self.fact_helper.create_casefact_declaration_monadic("has_company_expiration_date", "company", company_expirations)

        result += newline

        result += self.fact_helper.create_casefact_declaration_binary("shareholder_company", "shareholder", "company", [(get_cname_shareholder(x), cname_company) for x in shareholders])
        result += self.fact_helper.create_casefact_declaration_binary("shareholder_person", "shareholder", "person", [(get_cname_shareholder(x), get_cname_person(x)) for x in shareholders])

        if not self.configuration.precompute_arithmetics:
            result += self.fact_helper.create_casefact_declaration_binary("shareholder_votes", "shareholder", "$int", [(get_cname_shareholder(x), str(x['votes'])) for x in shareholders])

        result += newline

        directors_and_liquidators = self.get_directors_and_liquidators(input_data)

        result += self.fact_helper.create_casefact_declaration_binary("director_company", "director", "company", [(x, cname_company) for x, y in directors_and_liquidators])
        result += self.fact_helper.create_casefact_declaration_binary("director_person", "director", "person", [(x, get_cname_person(y)) for x, y in directors_and_liquidators])
        result += self.fact_helper.create_casefact_declaration_binary("director_representationpower", "director", "representationpower", [(x, y['representationpower']) for x, y in directors_and_liquidators if not is_empty(y.get('representationpower'))])
        result += self.fact_helper.create_casefact_declaration_monadic("director_exemption181", "director", [x for x, y in directors_and_liquidators if y.get('exemption181')])

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
                result += self._create_precomputed_majority_axiom(yes_votes, no_votes)
            else:
                if yes_votes is not None:
                    result += self.fact_helper.create_casefact_declaration_binary("voting_yesvotes", "voting", "$int", [(cname_voting, str(yes_votes))])
                if no_votes is not None:
                    result += self.fact_helper.create_casefact_declaration_binary("voting_novotes", "voting", "$int", [(cname_voting, str(no_votes))])
                if abstentions is not None:
                    result += self.fact_helper.create_casefact_declaration_binary("voting_abstentions", "voting", "$int", [(cname_voting, str(abstentions))])

            result += newline

        consents_to_teleconference = meeting.get('consent_to_teleconference')
        if consents_to_teleconference is None:
            consents_to_teleconference = []
        result += self.fact_helper.create_casefact_declaration_binary("does_shareholder_consent_to_teleconference_meeting", "meeting", "shareholder", [(get_cname_voting(), get_cname_shareholder(x)) for x in consents_to_teleconference])

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

        resolution_notarizations = []
        if resolution['notarized']:
            resolution_notarizations += [get_cname_resolution()]
        result += self.fact_helper.create_casefact_declaration_monadic("is_resolution_notarized", "resolution", resolution_notarizations)

        result += newline

        company_liquidators = company.get('liquidators')
        resolution_liquidators = resolution.get('liquidators')

        dirliq_cname_func = get_cname_director if company_liquidators is None and resolution_liquidators is None else get_cname_liquidator
        assurance_signers = [(get_cname_assurance(), dirliq_cname_func(x)) for x in assurance_signers]
        result += self.fact_helper.create_casefact_declaration_binary("assurance_signer", "assurance", "director", assurance_signers)

        result += self.fact_helper.create_casefact_declaration_binary("deed_format", "deed", "deedformat", [(get_cname_deed(), application['deed_format'])])

        applicants = application.get('applicants')
        result += self.fact_helper.create_casefact_declaration_binary("application_applicant", "application", "director", [(get_cname_application(), dirliq_cname_func(x)) for x in applicants])

        if company_liquidators is not None:
            result += self.fact_helper.create_casefact_declaration_binary_grouped(
                "liquidatorlist_liquidator", "liquidatorlist", "director",
                get_cname_liquidatorlist_AoA(), [get_cname_liquidator(x) for x in company_liquidators])

        if resolution_liquidators is not None:
            result += self.fact_helper.create_casefact_declaration_binary_grouped(
                "liquidatorlist_liquidator", "liquidatorlist", "director",
                get_cname_liquidatorlist_resolution(), [get_cname_liquidator(x) for x in resolution_liquidators])

        return result

    def _get_main_object_name(self, root_rule: str) -> str:
        if root_rule == "is_application_legal":
            return get_cname_application()

        raise Exception("no implementation provided for root rule " + root_rule)

    def _create_precomputed_majority_axiom(self, yes_votes: Union[str, None], no_votes: Union[str, None]) -> str:
        if yes_votes is None or no_votes is None:
            return ""

        yes_votes_int = int(yes_votes)
        no_votes_int = int(no_votes)

        majreq = 0.75  # ToDo: better extract this from the rules
        yes_ratio = yes_votes_int / (yes_votes_int + no_votes_int)
        is_majority = yes_ratio > majreq

        cname_res = get_cname_resolution()
        result = "% precomputed resolution majority: "
        result += "{:6.4f}".format(yes_ratio) + " > " + "{:6.4f}".format(majreq) + "?" + newline
        result += self.fact_helper.create_nonpredcompl_casefact_monadic("is_resolution_passed_via_voting", cname_res, not is_majority)
        return result

    def get_directors_and_liquidators(self, input_data: dict):
        company = input_data['company']
        resolution = input_data['resolution']
        directors = company['directors']

        directors_and_liquidators = []
        directors_and_liquidators += [(get_cname_director(x), x) for x in directors]

        company_liquidators = company.get('liquidators')
        if company_liquidators is not None:
            for liquidator in company_liquidators:
                directors_and_liquidators.append((get_cname_liquidator(liquidator), liquidator))

        resolution_liquidators = resolution.get('liquidators')
        if resolution_liquidators is not None:
            for liquidator in resolution_liquidators:
                directors_and_liquidators.append((get_cname_liquidator(liquidator), liquidator))

        return directors_and_liquidators

    def get_all_persons_cnames(self, shareholders, directors_and_liquidators) -> List[str]:
        names = []
        names += [get_cname_person(x) for x in shareholders]
        names += [get_cname_person(y) for x, y in directors_and_liquidators]

        names = list(dict.fromkeys(names))

        return names
