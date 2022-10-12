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

export const keyMatcher = {
  'Pays': 'country',
  'Region': 'canton',
  'Altitude': 'altitude',
  'Météo': 'meteoParam',
  'Context': 'context',
  'Typologie': 'typo',
  'Années de construction': 'year',
  'Catégorie d\'ouvrage': 'category',
  'Hauteur du bâtiment': 'height',
  'Type de chauffage': 'generator',
  'Année d\'installation du chauffage': 'generatorYear',
  'Type d\'émetteurs': 'emettors',
  'Régulation du chauffage': 'regulation',
  'Isolation des conduites de chauffage': 'tubeInsulH',
  'Isolation des conduites d\'ECS': 'tubeInsulW',
  'Présence d\'une installation solaire thermique': 'solarThermal',
  'Nombre de logements': 'nbAppart',
  'Efficacité des appareils électriques': 'devEff',
  'Présence d\'une ventilation mécanique': 'ventMeca',
  'Présence d\'ascenseur': 'elevator',
  'Présence d\'une instalaltion solaire PV': 'solarPV',
  'Présence de batteries de stockage': 'pvBattery',
  'Note de protection du patrimoine': 'renoLevel',
  'Capacité d\'investissement': 'renoMaxCost',
};
export const valueMatcher = {
  // "country":
  'Suisse': 'Suisse',
  'France': 'France',
  // "canton":
  'Valais': 'VS',
  'Vaud': 'VD',
  'Fribourg': 'FR',
  'Bern': 'BE',
  'Neuchâtel': 'NE',
  'Jura-CH': 'JU',
  'Genève': 'GE',
  'Haute-Savoie': '74',
  'Ain': '01',
  'Jura-FR': '39',
  'Territoire de Belfort': '90',
  // "meteoParam": {
  'Jura': 'jura',
  'Préalpes': 'preAlpes',
  'Dégagé vers le sud': 'sud',
  'Bouché vers le sud': 'norSud',
  // "context": {
  'Rural': 'rural',
  'Urban': 'urban',
  'Suburban': 'suburban',
  // "generator": {
  'Mazout': 'genTypOil',
  'Gas naturel': 'genTypGas',
  'Pellets': 'genTypWoodPellets',
  'Büches bois': 'genTypWoodLogs',
  'Vopeaux bois': 'genTypWoodChpis',
  'PAC air-eau': 'genTypHeatPumpAW',
  'PAC sol-eau': 'genTypHeatPumpGW',
  'Électrique direct': 'genTypElecDirect',
  'Chauffage à distance': 'genTypCAD',
  // "emettors": {
  'Radiateurs': 'emRadWall',
  'Radiateurs devant fenêtres': 'emRadWin',
  'Plancher(s) chaffant(s)': 'emHeatedFloor',
  'Murs chauffants': 'emHeatedWall',
  'Aucun (élec direct)': 'emNone',
  // "regulation": {
  'Par pièce (+0°C)': 0,
  'Par pièce de référence (+1°C)': 1,
  'autre (+2°C)': 2,
  // "tubeInsulW": {
  'Non isolées': 'notInsulated',
  'Partiellement isolées': 'partiallyInsulated',
  'Complètement isolées': 'fullyInsulated',
  // "devEff"
  'Meilleurs appareils': 'best',
  'Appareils neufs courants': 'new',
  'Anciens appareils (env. 5 ans)': 'old5',
  'Très anciens appareils (>10 ans)': 'old10',
  // "ventMeca"
  'Aucune': 'none',
  'Double flux': 'df',
  'Simple flux': 'sf',
  // 'boolean'
  'Non': 0,
  'Oui': 1,
};
export const keyOfValueMatcher = Object.keys(valueMatcher).sort();

export const postUrl = writable('');
