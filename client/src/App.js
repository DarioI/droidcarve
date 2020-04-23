import React from 'react';
import './App.css';
import {MainView, StartView} from './layouts';
import {ApplicationProvider, ApplicationContext, DeviceProvider} from './context/';

function getContent(application){

  if (application)
  {
    return <MainView />
  }
  else
  {
    return <StartView />
  }
}

function App() {
  return (
    <React.StrictMode>
        <ApplicationProvider>
          <DeviceProvider>
            <ApplicationContext.Consumer>
                      {context => 
                        getContent(context.application)
                      }
            </ApplicationContext.Consumer>
          </DeviceProvider>
        </ApplicationProvider>
    </React.StrictMode>
  );
}

export default App;
