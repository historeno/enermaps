import {writable} from 'svelte/store';

export const activeSelectionLayerStore = writable();
export const activeOverlayLayersStore= writable([]);
export const activeCMOutputLayersStore= writable([]);

export const selectionStore = writable();
export const layersStore = writable([]);
export const selectedLayer = writable();

export const isCMPaneActiveStore = writable(false);
