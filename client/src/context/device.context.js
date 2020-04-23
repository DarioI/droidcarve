import React from 'react';

import { deviceService } from '../services';
import { message } from 'antd';

export const DeviceContext = React.createContext({device: null});

export class DeviceProvider extends React.Component {

    state = {
      device: null
    }

    componentDidMount()
    {
      this.refresh()
    }

    connect(serial)
    {
      deviceService.connectDevice(serial)
        .then( result => result.data )
        .then( data => {this.refresh()})
        .catch( error => {
          message.error("Could not connect to "+serial)
        })
    }

    refresh()
    {
      deviceService.getCurrentDevice()
        .then(result => {
          this.setState({device: result.data.device})
        })
    }

    render() {
      return (
        <DeviceContext.Provider
          value={{
            device: this.state.device,
            connect: serial => {
              this.connect(serial)
            }
          }}
        >
          {this.props.children}
        </DeviceContext.Provider>
      );
    }
  }