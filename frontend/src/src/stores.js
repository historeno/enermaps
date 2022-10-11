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

export const consultdata = writable('Pas de données');

export const allFields = writable(null);
