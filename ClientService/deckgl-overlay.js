import React, {Component} from 'react';
import DeckGL, {ScatterplotLayer} from 'deck.gl';

const PICKUP_COLOR = [0, 128, 255];
const DROPOFF_COLOR = [255, 0, 128];

export default class DeckGLOverlay extends Component {

  render() {
    console.log(this.props.data.length);
    if (!this.props.data) {
      console.log("NO DATA??????");
      return null;
    }

    const layers = [
      new ScatterplotLayer({
        id: 'scatterplot',
        getPosition: d => d.position,
        getColor: d => d.grounded ? PICKUP_COLOR : DROPOFF_COLOR,
        getRadius: d => 5,
        opacity: 1,
        pickable: true,
        radiusMinPixels: 0.25,
        radiusMaxPixels: 30,
        ...this.props
      })
    ];

    return (
      <DeckGL {...this.props.viewport} layers={layers} />
    );
  }
}
