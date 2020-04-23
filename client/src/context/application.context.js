import React from 'react';
import { appService } from '../services';

export const ApplicationContext = React.createContext()

export class ApplicationProvider extends React.Component {

    constructor(props)
    {
      super(props)
      this.state = {
        application: null,
      };
    }

    componentDidMount()
    {
        appService.getCurrentApplication()
            .then(result => {
                if (!result.data.application) {
                  this.setState({application: null})
                }
                else {
                  this.setState({application: result.data})
                }
            })
    }

    render() {
      return (
        <ApplicationContext.Provider
          value={{
            application: this.state.application
          }}
        >
          {this.props.children}
        </ApplicationContext.Provider>
      );
    }
  }