import React from 'react';
import { List, message, Button } from 'antd';
import { RedoOutlined, ApiOutlined } from '@ant-design/icons';
import { deviceService } from '../../services';
import { DeviceContext } from '../../context/device.context';
import APKDownloader from './APKDownloader';

class ChooseAPK extends React.Component {

    constructor(props)
    {
        super(props)
        this.state = {
            loading: true,
            devices : [],
        }

        this.refresh = this.refresh.bind(this);
    }

    componentDidMount()
    {
        this.refresh()
    }

    refresh()
    {
        this.setState({loading: true})
        deviceService.getDevices()
            .then(result => result.data)
            .then(data => {
                if (!data.devices) { this.setState({ loading: false, devices: []})}
                else {
                    this.setState({loading: false, devices: data.devices.map(item => {
                            return ({
                                title: item.serial,
                                description: item.name
                            })
                        })});
                }
            })
            .catch(error => {
                this.setState({loading: false})
                message.error("Could not load devices.")
            })
    }


    getView(devContext)
    {
        if (!devContext.device)
        {
            return(
                <List
                    size="large"
                    itemLayout="horizontal"
                    bordered
                    loading={this.state.loading}
                    dataSource={this.state.devices}
                    footer={<div style={{textAlign: 'center'}}><Button type="primary" icon={<RedoOutlined />} onClick={this.refresh} size="small">refresh</Button></div>}
                    renderItem={item => (
                    <List.Item actions={[<Button key={item.title} type="primary" size="small" icon={<ApiOutlined />} onClick={() => {devContext.connect(item.title)}}>connect</Button>]}>
                        <List.Item.Meta
                            title={<span>{item.title}</span>}
                            description={<span>{item.description}</span>}
                        />
                    </List.Item>
                    )}
                />
            )
        }
        else{
            return(
                <APKDownloader />
            )
        }
    }
    render()
    {

        return(
            <DeviceContext.Consumer>
                {devContext =>
                    this.getView(devContext)
                }
            </DeviceContext.Consumer>
        )
    }
}

export default ChooseAPK;