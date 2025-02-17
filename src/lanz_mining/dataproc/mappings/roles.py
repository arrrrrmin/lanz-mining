# Roles mapping aims to resolve the diverse number of arbitary roles applied to people.
# Goal is to find aggreagtions that describe the data properly, without getting to detailed.
from lanz_mining.dataproc.mappings.types import as_rpattern, Group


group_activism_kws = [
    "aktivist",
    "bürgerrechtler",
    "whistleblow",
    "völkerrechtler",
    "nawalny",
    "boris-nemzow",
    "kreml-kritiker",
    "wwf",
    "letzte generation",
]
group_history_kws = ["historiker", "zeitzeuge", "zeitzeugin", "shoah"]
group_social_kws = [
    "soziolog",
    "sozialwissenschaft",
    "sozialpsycholog",
    "sozialarbeiter",
    "sprecher der arche",
    "sprecherin der arche",
    "gewerkschaft",
    "sozialverband",
    "tafel deutschland",
    "ethikrat",
]
group_education_kws = [
    "bildung",
    "lehrer",
    "pädagog",
    "schüler",
    "student",
    "schulleiter",
    "pädagog",
]
group_health_kws = [
    "arzt",
    "ärztin",
    "pharmazeut",
    "psychiater",
    "mediziner",
    "virolog",
    "psycholog",
    "gynäkolog",
    "pharmakolog",
    "gesundheit",
    "radiolog",
    "suchtexpert",
    "onkologe",
]
group_domestic_kws = [
    "sicherheitsexpert",
    "innere sicherheit",
    "sicherheitskonferenz",
    "polizei",
    "polizist",
    "kriminal",
    "migrationsexpert",
    "integrationsexpert",
    "kriminolog",
    "migrationswissenschaft",
    "mirgationsforscher",
    "integration",
    "flüchtlingsrat",
]
group_military_kws = [
    "militär",
    "verteidigung",
    "bundeswehr",
    "oberst",
    "agent",
    "leutnat",
    "kommandierende",
]
group_law_kws = [
    "jurist",
    "richter",
    "rechtsanwalt",
    "rechtsanwältin",
    "steuerexpert",
    "rechtsexpert",
]
group_science_kws = [
    "wissenschaft",
    "forscher",
    "physiker",
    "biolog",
    "hydrologe",
    "zukunftsforscher",
    "ökolog",
    "philosoph",
    "theolog",
    "politolog",
    "politikwissenschaft",
    "islamwissenschaft",
    "extremismusforscher",
    "institut",
    "hertie-stiftung",
]
group_literatur_kws = ["autor", "schriftsteller", "publizist"]
group_culture_kws = ["schauspieler", "musiker", "regisseur", "produzent", "sänger"]
group_international_kws = [
    "afrika",
    "asien",
    "china",
    "russland",
    "iran-expert",
    "amerika",
    "usa-expert",
    "nahost",
    "botschafter",
    "ukrain",
    "frankreich",
    "osteuropa",
    "türkei",
    "diplomat",
    "islam-expert",
    "kiew",
]
group_economy_kws = [
    "wirtschaft",
    "ökonom",
    "vorstand",
    "vw-chef",
    "manager",
    "industrie",
    "unternehmer",
    "unternehmensberater",
    "volkswirt",
    "zentralverbandes des deutschen handwerks",
    "industrie",
    "autoexperte",
    "aufsichtsratsvorsitzender .+ ag",
    "investor",
]
group_journalist_kws = [
    "reporter",
    "journalist",
    "korrespondent",
    "kolumnist",
    "redakteur",
    "redaktion",
    "zdf",
    "ard",
    "hauptstadtbüro",
    "ressort",
    "herausgeber",
    "politik-expert",
    "rheinische post",
    "chefredakteur",
]


GROUP_MAPS: dict[str, str] = {
    Group.Activism: as_rpattern(group_activism_kws),
    Group.History: as_rpattern(group_history_kws),
    Group.Social: as_rpattern(group_social_kws),
    Group.Education: as_rpattern(group_education_kws),
    Group.Health: as_rpattern(group_health_kws),
    Group.Domestic: as_rpattern(group_domestic_kws),
    Group.Military: as_rpattern(group_military_kws),
    Group.Law: as_rpattern(group_law_kws),
    Group.Science: as_rpattern(group_science_kws),
    Group.Literatur: as_rpattern(group_literatur_kws),
    Group.Culture: as_rpattern(group_culture_kws),
    Group.International: as_rpattern(group_international_kws),
    Group.Economy: as_rpattern(group_economy_kws),
    Group.Journalist: as_rpattern(group_journalist_kws),
    # Group.Politician: group_politician_kws,
}
