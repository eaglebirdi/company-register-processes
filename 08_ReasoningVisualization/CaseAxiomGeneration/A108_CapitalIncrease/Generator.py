from typing import List
from Reasoning_Visualization import NamedFile
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
        result_inst = ""
        result_rel = ""

        company = input_data['company']
        application = input_data['application']
        result_inst += self.inst_helper.create_instance_declaration(get_cname_company(), "company")
        result_inst += self.inst_helper.create_instance_declaration(get_cname_application(), "application")
        result_inst += self.inst_helper.create_instance_declaration(get_cname_assurance(), "assurance")
        result_inst += self.inst_helper.create_instance_declaration(get_cname_amendedAoA(), "amendedAoA")
        result_inst += self.inst_helper.create_instance_declaration(get_cname_subscriberlist(), "subscriberlist")

        result_rel += self.inst_helper.create_relation_declaration("application_assurance", "application", "assurance", get_cname_application(), get_cname_assurance())
        result_rel += self.inst_helper.create_relation_declaration("application_amendedAoA", "application", "amendedAoA", get_cname_application(), get_cname_amendedAoA())
        result_rel += self.inst_helper.create_relation_declaration("application_subscriberlist", "application", "subscriberlist", get_cname_application(), get_cname_subscriberlist())

        ci_resolution = input_data['capital_increase_resolution']
        ci_meeting = ci_resolution['meeting']
        ci_voting = ci_resolution.get('voting')

        result_rel += self.inst_helper.create_relation_declaration("application_capitalincreaseresolution", "application", "capitalincreaseresolution", get_cname_application(), get_cname_ci_resolution())
        result_rel += self.inst_helper.create_relation_declaration("company_capitalincreaseresolution", "company", "capitalincreaseresolution", get_cname_company(), get_cname_ci_resolution())

        result_inst += self.inst_helper.create_instance_declaration(get_cname_ci_resolution(), "capitalincreaseresolution")
        if ci_meeting['occurred']:
            result_inst += self.inst_helper.create_instance_declaration(get_cname_ci_meeting(), "meeting")
            result_rel += self.inst_helper.create_relation_declaration("capitalincreaseresolution_meeting", "capitalincreaseresolution", "meeting", get_cname_ci_resolution(), get_cname_ci_meeting())
        if ci_voting is not None:
            result_inst += self.inst_helper.create_instance_declaration(get_cname_ci_voting(), "voting")
            result_rel += self.inst_helper.create_relation_declaration("capitalincreaseresolution_voting", "capitalincreaseresolution", "voting", get_cname_ci_resolution(), get_cname_ci_voting())

        all_shareholders_names = []

        per_resolution = input_data.get('permit_resolution')
        if per_resolution is not None:
            result_inst += self.inst_helper.create_instance_declaration(get_cname_per_resolution(), "permitresolution")
            result_rel += self.inst_helper.create_relation_declaration("application_permitresolution", "application", "permitresolution", get_cname_application(), get_cname_per_resolution())
            per_meeting = per_resolution['meeting']
            if per_meeting['occurred']:
                result_inst += self.inst_helper.create_instance_declaration(get_cname_per_meeting(), "meeting")
                result_rel += self.inst_helper.create_relation_declaration("permitresolution_meeting", "permitresolution", "meeting", get_cname_per_resolution(), get_cname_per_meeting())
            per_voting = per_resolution.get('voting')
            if per_voting is not None:
                result_inst += self.inst_helper.create_instance_declaration(get_cname_per_voting(), "voting")
                result_rel += self.inst_helper.create_relation_declaration("permitresolution_voting", "permitresolution", "voting", get_cname_per_resolution(), get_cname_per_voting())

            for admitted in per_resolution['admitted_shareholders']:
                all_shareholders_names.append(admitted)

        shareholders = company['shareholders']
        for shareholder in shareholders:
            shareholder_name = shareholder['name']
            if shareholder_name not in all_shareholders_names:
                all_shareholders_names.append(shareholder_name)

        subscriber_list = application['subscriber_list']
        all_shareholders_names += [x['name'] for x in subscriber_list if x['name'] not in all_shareholders_names]

        for shareholder_name in all_shareholders_names:
            result_inst += self.inst_helper.create_instance_declaration(get_cname_shareholder(shareholder_name), "shareholder")

        directors = company['directors']
        for director in directors:
            result_inst += self.inst_helper.create_instance_declaration(get_cname_director(director), "director")

        persons = self.get_all_persons_cnames(all_shareholders_names, directors)
        for person_cname in persons:
            result_inst += self.inst_helper.create_instance_declaration(person_cname, "person")

        for subscription in subscriber_list:
            result_inst += self.inst_helper.create_instance_declaration(get_cname_subscription(subscription), "subscription")

        declarations = application['declarations']
        for declaration in declarations:
            result_inst += self.inst_helper.create_instance_declaration(get_cname_declaration(declaration), "declaration")

        result_inst += newline
        result_inst += self.inst_helper.create_inequality_constraints(persons)
        result_inst += newline
        result_inst += self.inst_helper.create_inequality_constraints([get_cname_shareholder(x) for x in all_shareholders_names])
        result_inst += newline
        directors_names = [get_cname_director(x) for x in directors]
        result_inst += self.inst_helper.create_inequality_constraints(directors_names)
        result_inst += newline
        if per_resolution is not None:
            if per_resolution['meeting']['occurred']:
                result_inst += self.inst_helper.create_inequality_constraints([get_cname_ci_meeting(), get_cname_per_meeting()])
                result_inst += newline
            per_voting = per_resolution.get('voting')
            if per_voting is not None:
                result_inst += self.inst_helper.create_inequality_constraints([get_cname_ci_voting(), get_cname_per_voting()])
                result_inst += newline
        declaration_names = [get_cname_declaration(x) for x in declarations]
        result_inst += self.inst_helper.create_inequality_constraints(declaration_names)
        result_inst += newline
        subscription_names = [get_cname_subscription(x) for x in subscriber_list]
        result_inst += self.inst_helper.create_inequality_constraints(subscription_names)

        return result_inst + newline + result_rel

    def _create_casefacts_axioms(self, input_data: dict) -> str:
        result = ""

        company = input_data['company']
        application = input_data['application']
        amended_AoA = application['amended_AoA']
        applicants = application['applicants']

        contains_AoA_full_text = []
        if application['contains_AoA_full_text']:
            contains_AoA_full_text += [get_cname_application()]
        result += self.fact_helper.create_casefact_declaration_monadic("contains_AoA_full_text", "application", contains_AoA_full_text)

        has_increased_capital_been_covered = []
        if application['has_increased_capital_been_covered']:
            has_increased_capital_been_covered += [get_cname_application()]
        result += self.fact_helper.create_casefact_declaration_monadic("has_increased_capital_been_covered", "application", has_increased_capital_been_covered)

        result += self.fact_helper.create_casefact_declaration_binary("application_applicant", "application", "director", [(get_cname_application(), get_cname_director(x)) for x in applicants])

        matches_notarily_certified = []
        if amended_AoA['matches_notarily_certified']:
            matches_notarily_certified += [get_cname_application()]
        result += self.fact_helper.create_casefact_declaration_monadic("are_matches_notarily_certified", "application", matches_notarily_certified)

        result += self.fact_helper.create_casefact_declaration_binary("amendedAoA_formercapital", "amendedAoA", "$int", [(get_cname_amendedAoA(), str(amended_AoA['former_capital']))])
        result += self.fact_helper.create_casefact_declaration_binary("amendedAoA_increase", "amendedAoA", "$int", [(get_cname_amendedAoA(), str(amended_AoA['increase']))])
        result += self.fact_helper.create_casefact_declaration_binary("amendedAoA_newcapital", "amendedAoA", "$int", [(get_cname_amendedAoA(), str(amended_AoA['new_capital']))])

        assurance_signed = []
        if application['assurance_signed']:
            assurance_signed += [get_cname_assurance()]
        result += self.fact_helper.create_casefact_declaration_monadic("is_assurance_signed", "assurance", assurance_signed)


        ci_resolution = input_data['capital_increase_resolution']
        ci_meeting = ci_resolution['meeting']
        ci_voting = ci_resolution.get('voting')

        consents_to_teleconference = []
        meeting_format = []
        voting_yesvotes = []
        voting_novotes = []
        voting_abstentions = []

        written_consents_ci = ci_resolution.get('written_consents')
        if written_consents_ci is None:
            written_consents_ci = []
        result += self.fact_helper.create_casefact_declaration_binary("does_shareholder_consent_to_the_determination_ci", "capitalincreaseresolution", "shareholder", [(get_cname_ci_resolution(), get_cname_shareholder(x)) for x in written_consents_ci])

        consents_to_voting_in_writing_ci = ci_resolution.get('consents_to_voting_in_writing')
        if consents_to_voting_in_writing_ci is None:
            consents_to_voting_in_writing_ci = []
        result += self.fact_helper.create_casefact_declaration_binary("does_shareholder_consent_to_voting_in_writing_ci", "capitalincreaseresolution", "shareholder", [(get_cname_ci_resolution(), get_cname_shareholder(x)) for x in consents_to_voting_in_writing_ci])

        is_capitalincrease_resolution_notarized = []
        if ci_resolution['notarized']:
            is_capitalincrease_resolution_notarized += [get_cname_ci_resolution()]
        result += self.fact_helper.create_casefact_declaration_monadic("is_capitalincreaseresolution_notarized", "capitalincreaseresolution", is_capitalincrease_resolution_notarized)

        if ci_meeting['occurred']:
            consents_to_teleconference_ci = ci_meeting.get('consents_to_teleconference')
            if consents_to_teleconference_ci is not None:
                consents_to_teleconference += [(get_cname_ci_meeting(), get_cname_shareholder(x)) for x in consents_to_teleconference_ci]

            if not is_empty(ci_meeting['format']):
                meeting_format.append((get_cname_ci_meeting(), ci_meeting['format']))
        if ci_voting is not None:
            ci_voting_yesvotes = ci_voting.get('yes_votes')
            if ci_voting_yesvotes is not None:
                voting_yesvotes.append((get_cname_ci_voting(), str(ci_voting_yesvotes)))
            ci_voting_novotes = ci_voting.get('no_votes')
            if ci_voting_novotes is not None:
                voting_novotes.append((get_cname_ci_voting(), str(ci_voting_novotes)))
            ci_voting_abstentions = ci_voting.get('abstentions')
            if ci_voting_abstentions is not None:
                voting_abstentions.append((get_cname_ci_voting(), str(ci_voting_abstentions)))

        all_shareholders_names = []

        per_resolution = input_data.get('permit_resolution')
        if per_resolution is not None:

            written_consents_per = per_resolution.get('written_consents')
            if written_consents_per is None:
                written_consents_per = []
            result += self.fact_helper.create_casefact_declaration_binary("does_shareholder_consent_to_the_determination_per", "permitresolution", "shareholder", [(get_cname_per_resolution(), get_cname_shareholder(x)) for x in written_consents_per])

            consents_to_voting_in_writing_per = per_resolution.get('consents_to_voting_in_writing')
            if consents_to_voting_in_writing_per is None:
                consents_to_voting_in_writing_per = []
            result += self.fact_helper.create_casefact_declaration_binary("does_shareholder_consent_to_voting_in_writing_per", "permitresolution", "shareholder", [(get_cname_per_resolution(), get_cname_shareholder(x)) for x in consents_to_voting_in_writing_per])

            per_meeting = per_resolution['meeting']
            if per_meeting['occurred']:
                consents_to_teleconference_per = per_meeting.get('consents_to_teleconference')
                if consents_to_teleconference_per is not None:
                    consents_to_teleconference += [(get_cname_per_meeting(), get_cname_shareholder(x)) for x in consents_to_teleconference_per]

                if not is_empty(per_meeting['format']):
                    meeting_format.append((get_cname_per_meeting(), per_meeting['format']))

            per_voting = per_resolution.get('voting')
            if per_voting is not None:
                per_voting_yesvotes = per_voting.get('yes_votes')
                if per_voting_yesvotes is not None:
                    voting_yesvotes.append((get_cname_per_voting(), str(per_voting_yesvotes)))
                per_voting_novotes = per_voting.get('no_votes')
                if per_voting_novotes is not None:
                    voting_novotes.append((get_cname_per_voting(), str(per_voting_novotes)))
                per_voting_abstentions = per_voting.get('abstentions')
                if per_voting_abstentions is not None:
                    voting_abstentions.append((get_cname_per_voting(), str(per_voting_abstentions)))

            result += self.fact_helper.create_casefact_declaration_binary("permitresolution_shareholder", "permitresolution", "shareholder", [(get_cname_per_resolution(), get_cname_shareholder(x)) for x in per_resolution['admitted_shareholders']])

            for shareholder in per_resolution['admitted_shareholders']:
                all_shareholders_names.append(shareholder)

        result += self.fact_helper.create_casefact_declaration_binary("does_shareholder_consent_to_teleconference_meeting", "meeting", "shareholder", consents_to_teleconference)
        result += self.fact_helper.create_casefact_declaration_binary("meeting_format", "meeting", "meetingformat", meeting_format)
        result += self.fact_helper.create_casefact_declaration_binary("voting_yesvotes", "voting", "$int", voting_yesvotes)
        result += self.fact_helper.create_casefact_declaration_binary("voting_novotes", "voting", "$int", voting_novotes)
        result += self.fact_helper.create_casefact_declaration_binary("voting_abstentions", "voting", "$int", voting_abstentions)


        shareholders = company['shareholders']
        all_shareholders_names += [x['name'] for x in shareholders]

        subscriber_list = application['subscriber_list']
        all_shareholders_names += [x['name'] for x in subscriber_list if x['name'] not in all_shareholders_names]

        result += self.fact_helper.create_casefact_declaration_binary("shareholder_company", "shareholder", "company", [(get_cname_shareholder(x), get_cname_company()) for x in shareholders])
        result += self.fact_helper.create_casefact_declaration_binary("shareholder_person", "shareholder", "person", [(get_cname_shareholder(x), get_cname_person(x)) for x in all_shareholders_names])
        result += self.fact_helper.create_casefact_declaration_binary("shareholder_votes", "shareholder", "$int", [(get_cname_shareholder(x), str(x['votes'])) for x in shareholders])

        directors = company['directors']
        result += self.fact_helper.create_casefact_declaration_binary("director_company", "director", "company", [(get_cname_director(x), get_cname_company()) for x in directors])
        result += self.fact_helper.create_casefact_declaration_binary("director_person", "director", "person", [(get_cname_director(x), get_cname_person(x)) for x in directors])

        result += self.fact_helper.create_casefact_declaration_binary("subscriberlist_subscription", "subscriberlist", "subscription", [(get_cname_subscriberlist(), get_cname_subscription(x)) for x in subscriber_list])
        result += self.fact_helper.create_casefact_declaration_binary("subscription_shareholder", "subscription", "shareholder", [(get_cname_subscription(x), get_cname_shareholder(x)) for x in subscriber_list])
        result += self.fact_helper.create_casefact_declaration_binary("subscription_shares", "subscription", "$int", [(get_cname_subscription(x), str(x['shares'])) for x in subscriber_list])

        declarations = application['declarations']
        result += self.fact_helper.create_casefact_declaration_binary("application_declaration", "application", "declaration", [(get_cname_application(), get_cname_declaration(x)) for x in declarations])
        result += self.fact_helper.create_casefact_declaration_binary("declaration_shareholder", "declaration", "shareholder", [(get_cname_declaration(x), get_cname_shareholder(x)) for x in declarations])
        result += self.fact_helper.create_casefact_declaration_binary("declaration_format", "declaration", "declarationformat", [(get_cname_declaration(x), x['format']) for x in declarations])
        result += self.fact_helper.create_casefact_declaration_monadic("is_declaration_notarized", "declaration", [get_cname_declaration(x) for x in declarations if x['notarized']])

        return result

    def _get_main_object_name(self, root_rule: str) -> str:
        if root_rule == "is_application_legal":
            return get_cname_application()

        raise Exception("no implementation provided for root rule " + root_rule)

    def get_all_persons_cnames(self, shareholders_names, directors) -> List[str]:
        names = []
        names += [get_cname_person(x) for x in shareholders_names]
        names += [get_cname_person(x) for x in directors]

        names = list(dict.fromkeys(names))

        return names
