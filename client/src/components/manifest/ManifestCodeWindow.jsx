import React from 'react';
import {UnControlled as CodeMirror} from 'react-codemirror2';
import { manifestService } from '../../services';
import { Alert, Card, message } from 'antd';

require('codemirror/lib/codemirror.css');
require('codemirror/theme/material.css');
require('codemirror/mode/xml/xml');


export class ManifestCodeWindow extends React.Component {

    constructor(props)
    {
        super(props)
        this.state = {
            error: false,
            loading: true,
            manifest: null
        }
    }

    componentDidMount() {
        manifestService.getManifestXML()
            .then(result => result.data)
            .then(data => {
                if (!data.xml)
                {
                    this.setState({error: true, loading: false})
                }
                else
                {
                    this.setState({manifest: data.xml, loading: false})
                }
            })
            .catch(error => {
                message.error('Could not load AndroidManifest.xml')
            })
    }

    render()
    {
        const {loading, error, manifest} = this.state;

        if (error || !manifest)
        {
            return <Alert type="error">Could not load AndroidManifest.xml</Alert>
        }

        return(
            <Card loading={loading}>
                <CodeMirror
                    style={{minHeight: 600, overflow: 'scroll'}}
                    value={this.state.manifest}
                    options={{
                        mode: {name: "xml"},
                        theme: 'material',
                        lineNumbers: true,
                        readOnly: true
                    }}
                    onChange={(editor, data, value) => {
                    }}
                />
            </Card>
        )
    }
}