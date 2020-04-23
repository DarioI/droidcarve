import React from 'react';
import { List } from 'antd';
import {AndroidOutlined} from '@ant-design/icons';
import { DeviceContext } from '../../context/device.context';

class DeviceInfo extends React.Component {

    constructor(props)
    {
        super(props)
        this.state = {
            device : []
        }

    }

    getDeviceData(device)
    {
        return [
            {
                title: <b>Serial</b>,
                description: device.serial
            },
            {
                title: <b>Name</b>,
                description: device.name
            },
            {
                title: <b>Manufacturer</b>,
                description: device.manufacturer
            },
            {
                title: <b>Model</b>,
                description: device.model
            },
            {
                title: <b>Android Version</b>,
                description: device.android_version
            },
            {
                title: <b>API Level</b>,
                description: device.api_level
            },
            {
                title: <b>CPU Architecture</b>,
                description: device.cpu_arch
            },
            {
                title: <b>CPU ABI</b>,
                description: device.cpu_abi
            },
            {
                title: <b>Crypto State</b>,
                description: device.crypto_state
            },
            {
                title: <b>FDE Algorithm</b>,
                description: device.fde_algorithm
            },
            {
                title: <b>Latest Security Patch</b>,
                description: device.latest_security_patch
            }
        ]
    }

    render()
    {

        return(
            <DeviceContext.Consumer>
                {context =>
                    <List
                        grid={{ gutter: 24, column: 4 }}
                        size="small"
                        itemLayout="horizontal"
                        bordered
                        loading={this.state.loading}
                        dataSource={this.getDeviceData(context.device)}
                        renderItem={item => (
                        <List.Item>
                            <List.Item.Meta
                                avatar={<AndroidOutlined />}
                                title={item.title}
                                description={item.description}
                            />
                        </List.Item>
                        )}
                    />
                }
            </DeviceContext.Consumer>
        )
    }
}

export default DeviceInfo;