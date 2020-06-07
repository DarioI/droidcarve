import React from 'react';
import {UnControlled as CodeMirror} from 'react-codemirror2';
import { installSmaliMode } from '../../utils/smali_mode.utils';
import { fileService } from '../../services/file.service';

require('codemirror/lib/codemirror.css');
require('codemirror/theme/material.css');

const Editor = require('codemirror/lib/codemirror.js');
installSmaliMode(Editor);

class CodeWindow extends React.Component {

    constructor(props)
    {
        super(props)
        this.state = {
            file: null
        }
    }

    componentDidMount() {

        if (this.props.lineNumbers)
        {
            this.setState({lineNumber: this.props.lineNumber})
        }
        if (!this.props.fileKey) return;

        fileService.getFile(this.props.fileKey)
            .then(result => {
                this.setState({file: result.data})
            })

    }

    render()
    {

        return(
            <CodeMirror
                    style={{minHeight: 600, overflow: 'scroll'}}
                    value={this.state.file ? this.state.file : 'Please select a file'}
                    options={{
                        mode: {name: "smali"},
                        theme: 'material',
                        lineNumbers: true,
                        readOnly: true
                    }}
                    onChange={(editor, data, value) => {
                    }}
                />
        )
    }
}

export default CodeWindow;