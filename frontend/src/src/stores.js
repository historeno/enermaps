import {writable} from 'svelte/store';

export const datasetsStore = writable([]);
export const datasetTopicsStore = writable([]);

export const areaSelectionStore = writable(null);
export const areaSelectionLayerStore = writable(null);

export const layersStore = writable([]);
export const selectedLayerStore = writable(null);

export const tasksStore = writable([]);

export const isCMPaneActiveStore = writable(false);

export const popupInformation = writable('Pas de données');

export const popupInformationtitle = writable('Infos générales');
export const allFormData = writable(null);

export const matcher = {
    'Pays': "country",
    'Region': "canton",
    'Altitude': "altitude",
    'Météo': "meteoParam",
    'Context': "context",
    'Typologie': "typo",
    'Années de construction': "year",
    'Catégorie d\'ouvrage': "category",
    'Hauteur du bâtiment': "height",
    'Type de chauffage': "generator",
    'Année d\'installation du chauffage': "generatorYear",
    'Type d\'émetteurs': "emettors",
    'Régulation du chauffage': "regulation",
    'Isolation des conduites de chauffage': "tubeInsulH",
    'Isolation des conduites d\'ECS': "tubeInsulW",
    'Présence d\'une installation solaire thermique': "solarThermal",
    'Nombre de logements': "nbAppart",
    'Efficacité des appareils électriques': "devEff",
    'Présence d\'une ventilation mécanique': "ventMeca",
    'Présence d\'ascenseur': "elevator",
    'Présence d\'une instalaltion solaire PV': "solarPV",
    'Présence de batteries de stockage': "pvBattery",
    'Note de protection du patrimoine': "renoLevel",
    'Capacité d\'investissement': "renoMaxCost",
};

export const postUrl = writable("");