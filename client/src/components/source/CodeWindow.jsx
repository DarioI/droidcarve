import React from 'react';
import {UnControlled as CodeMirror} from 'react-codemirror2';
import { installSmaliMode } from '../../utils/smali_mode.utils';
import { fileService } from '../../services/file.service';
import { ext } from '../../utils/files.utils';

require('codemirror/lib/codemirror.css');
require('codemirror/theme/material.css');
require('codemirror/mode/javascript/javascript');

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

        var mode = 'null';

        if (this.props.filename)
        {
            mode = this.getModeFromExtension(ext(this.props.filename))
        }

        if (!this.props.fileKey) return;

        fileService.getFile(this.props.fileKey)
            .then(result => {
                this.setState({file: result.data, mode: mode})
            })

    }

    getModeFromExtension(extension)
    {
        if (!extension) {
            return "null"
        }

        if (extension === "properties")
        {
            return "javascript"
        }

        if (extension === "json")
        {
            return "javascript"
        }

        if (extension === "version")
        {
            return "null"
        }

        return "null"

    }

    render()
    {

        return(
            <CodeMirror
                    style={{minHeight: 600, overflow: 'scroll'}}
                    value={this.state.file ? this.state.file : 'Please select a file'}
                    options={{
                        mode: {name: this.state.mode},
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