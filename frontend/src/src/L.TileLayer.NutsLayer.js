L.TileLayer.NutsLayer = L.TileLayer.WMS.extend({
  onAdd: function (map) {
    this.selection = L.geoJSON();
    this.selection.style = myStyle;
    this.selection.addTo(this._map);
    // Triggered when the layer is added to a map.
    //   Register a click listener, then do all the upstream WMS things
    L.TileLayer.WMS.prototype.onAdd.call(this, map);
    map.on("click", this.getFeatureInfo, this);
  },

  onRemove: function (map) {
    // Triggered when the layer is removed from a map.
    //   Unregister a click listener, then do all the upstream WMS things
    L.TileLayer.WMS.prototype.onRemove.call(this, map);
    map.off("click", this.getFeatureInfo, this);
    this._map.removeLayer(this.selection);
    this.selection = undefined;
  },
  getSelection: function() {
      return this.selection.toGeoJSON();
  },
  getFeatureInfo: function (evt) {
    let point = this._map.latLngToContainerPoint(evt.latlng, this._map.getZoom());

    let url = this.getFeatureInfoUrl(point);
    const showResults = L.Util.bind(this.onClickSelect, this);
    fetch(url).then(response => response.json()).catch((error) => {
	  console.error('Error:', error);
	}).then(data => {
	    showResults(undefined, data);
    });
  },

  getFeatureInfoUrl: function (point) {
       // Construct a GetFeatureInfo request URL given a point
      //TODO this one is way trickier than it seems for WMS 1.1.1 vs 1.3.0,
      // currently the backend and the frontend understand that:  
      // * the bounding box in the map coordinate
      // * the X and Y position are pixels offset
      // This behaviour changes between WMS version, so verify that the backend is 
      // talking version 1.1.1 of the WMS
      const size = this._map.getSize();
      const crs = this._map.options.crs;
      const mapBounds =  this._map.getBounds();
      const nw = crs.project(mapBounds.getNorthWest());
      const se = crs.project(mapBounds.getSouthEast());
      let params = {
        request: "GetFeatureInfo",
        service: "WMS",
        srs: crs.code,
        styles: this.wmsParams.styles,
        transparent: this.wmsParams.transparent,
        version: this.wmsParams.version,
        format: this.wmsParams.format,
        bbox: nw.x + ',' + se.y + ',' + se.x + ',' + nw.y,
        height: size.y,
        width: size.x,
        layers: this.wmsParams.layers,
        query_layers: this.wmsParams.layers,
        info_format: "application/json",
      };
    if (!!this.wmsParams.cql_filter) {
      params.cql_filter = this.wmsParams.cql_filter;
    }

    params[params.version === "1.3.0" ? "i" : "x"] = Math.floor(point.x);
    params[params.version === "1.3.0" ? "j" : "y"] = Math.floor(point.y);

    return this._url + L.Util.getParamString(params, this._url, true);
  },
  getFeatureId: function (feature) {
    if (!!feature.properties.nuts_id) {
      return feature.properties.nuts_id;
    }
    return feature.id;
  },
  onError: function (err) {
    console.log(err);
  },
  onClickSelect: function (err, content) {
    //if (err) { console.log(err); return; } // do nothing if there's an error
    // Otherwise show the content in a popup, or something.
    //this._map.getLayer("selection")
    const myStyle = {
      color: "#ff7800",
      weight: 10,
      opacity: 1,
    };
    //check if we already clicked to toggle the selection
    console.log("check click");
    //this._map.removeLayer(this.selection);
    //to be replaced by a dict to find the data per id
    for (const i in content.features) {
      const feature = content.features[i];
      const new_feature_id = this.getFeatureId(feature);
      var layer_removed = false;
      this.selection.eachLayer((layer) => {
        const feature_id = this.getFeatureId(layer.feature);
        if (new_feature_id == feature_id) {
          this.selection.removeLayer(layer);
          layer_removed = true;
        }
      });
      if (!layer_removed) {
        this.selection.addData(feature);
      }
    }
    //this.selection_by_id[content.properties.nuts_id] = content;
    console.log(this.selection.toGeoJSON().features.map(this.getFeatureId));
    //this.selection = L.geoJSON(content, {style: myStyle});
    //this.selection.id = "selection";
  },
});

L.tileLayer.nutsLayer = function (url, options) {
  return new L.TileLayer.NutsLayer(url, options);
};
