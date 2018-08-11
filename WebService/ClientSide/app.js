/* global window */
import React, {Component} from 'react';
import MapGL from 'react-map-gl';
import DeckGLOverlay from './deckgl-overlay';
import {LayerControls, SCATTERPLOT_CONTROLS} from './layer-controls';
import {tooltipStyle} from './style';
import taxiData from '../../../data/taxi';

const MAPBOX_STYLE = 'mapbox://styles/mapbox/dark-v9';
// Set your mapbox token here
const MAPBOX_TOKEN = process.env.MapboxAccessToken; // eslint-disable-line
const MY_DATA = [];

export default class App extends Component {

  constructor(props) {
    super(props);
    this.state = {
      viewport: {
        width: window.innerWidth,
        height: window.innerHeight,
        longitude: -74,
        latitude: 40.7,
        zoom: 11,
        maxZoom: 16
      },
      points: [],
      settings: Object.keys(SCATTERPLOT_CONTROLS).reduce((accu, key) => ({
        ...accu,
        [key]: SCATTERPLOT_CONTROLS[key].value
      }), {}),
      // hoverInfo
      x: 0,
      y: 0,
      hoveredObject: null,
      status: 'LOADING'
    };
    this._resize = this._resize.bind(this);
		//Starts websocket (hopefully only once)
		console.log("Starting websocket")
    this._getData = this._getData.bind(this);
    this._processData = this._processData.bind(this);
    this._getData();
  }

  componentDidMount() {
    this._processData();
    window.addEventListener('resize', this._resize);
    this._resize();
  }

  componentWillUnmount() {
    window.removeEventListener('resize', this._resize);
  }

  _processData() {
    if (MY_DATA) {
      console.log(MY_DATA.length);
      this.setState({status: 'LOADED'});
      const points = MY_DATA.reduce((accu, curr) => {
        accu.push({
          position: [Number(curr.Long), Number(curr.Lat)],
          grounded: true
        });

        return accu;
      }, []);
      console.log("POINTS:");
      console.log(points);
      this.setState({
        points,
        status: 'READY'
      });
      console.log(points);
    }
  }
  _getData() {
    //START WEB SOCKET
		console.log("INSIDE WEB SOCKET");
    //var host = window.location.host;
    var app = this;
    var ws = new WebSocket('ws://localhost:8888/ws');
    ws.onopen = function(){
      console.log("SOCKET_OPEN");
    };
    ws.onmessage = function(ev){
      var json = JSON.parse(ev.data);
      MY_DATA.push(json);
      console.log("PUSHING");

      if (MY_DATA.length%1000 == 0){
        console.log("Processing");
        app._processData();
      }
    };
    ws.onclose = function(ev){
      console.log("SOCKET CLOSED");
    };
    ws.onerror = function(ev){
    };
    //END WEB SOCKET
  }
	sleep(milliseconds) {
		var start = new Date().getTime();
		for (var i = 0; i < 1e7; i++) {
			if ((new Date().getTime() - start) > milliseconds){
				break;
			}
		}
	}
  _onHover({x, y, object}) {
    this.setState({x, y, hoveredObject: object});
  }

  _onViewportChange(viewport) {
    this.setState({
      viewport: {...this.state.viewport, ...viewport}
    });
  }

  _resize() {
    this._onViewportChange({
      width: window.innerWidth,
      height: window.innerHeight
    });
  }

  _updateLayerSettings(settings) {
    this.setState({settings});
  }

  render() {
    console.log("This is rendering so this is great");
    return (
      <div>
        {this.state.hoveredObject &&
          <div style={{
            ...tooltipStyle,
            transform: `translate(${this.state.x}px, ${this.state.y}px)`
          }}>
            <div>{JSON.stringify(this.state.hoveredObject)}</div>
          </div>}
        <LayerControls
          settings={this.state.settings}
          propTypes={SCATTERPLOT_CONTROLS}
          onChange={settings => this._updateLayerSettings(settings)}/>
        <MapGL
          {...this.state.viewport}
          mapStyle={MAPBOX_STYLE}
          onViewportChange={viewport => this._onViewportChange(viewport)}
          mapboxApiAccessToken={MAPBOX_TOKEN}>
          <DeckGLOverlay
            viewport={this.state.viewport}
            data={this.state.points}
            onHover={hover => this._onHover(hover)}
            {...this.state.settings}
          />
        </MapGL>
      </div>
    );
  }
}


