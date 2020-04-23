import React from 'react';
import { Upload, message } from 'antd';
import { AndroidOutlined } from '@ant-design/icons';
import { apiConstants } from '../../constants/api.constants';
import Loader from 'react-loader-spinner'

import "react-loader-spinner/dist/loader/css/react-spinner-loader.css"

const { Dragger } = Upload;


class APKUploader extends React.Component {

    constructor(props) {
        super(props)
        this.state = {
            application: null,
            current: 0,
            uploading: false
        }

        this.transformFile = this.transformFile.bind(this);
        this.onChange = this.onChange.bind(this);
    }

    transformFile(file) {
      this.setState({ uploading: true})
      return file;
    }

    onChange(info)
    {
      const { status } = info.file;
      if (status === 'done') {
        this.props.onDone()
      } else if (status === 'error') {
        this.setState({uploading: false})
        message.error(`${info.file.name} file upload failed.`);
      }

    }

    render()
    {
        const {uploading} = this.state;

        const props = {
          accept: '.apk',
          name: 'file',
          multiple: false,
          showUploadList: false,
          action: apiConstants.SET_CURRENT_APPLICTION,
          onChange: this.onChange,
          transformFile: this.transformFile

        };


        return(
                <Dragger {...props}>
                  {uploading &&
                  <div>
                    <Loader style={{padding: "20px"}}
                      type="Bars"
                      color="#00BFFF"
                      height={60}
                      width={60}
                      timeout={0}
                    />
                    <p className="ant-upload-text">Please wait until the APK is analyzed.</p>
                    </div>
                  }
                  {!uploading &&
                    <div>
                        <p className="ant-upload-drag-icon">
                        <AndroidOutlined />
                        </p>
                        <p className="ant-upload-text">Click or drag an .APK file to start analysis</p>
                    </div>
                  }
                </Dragger>


        )
    }
}

export default APKUploader;