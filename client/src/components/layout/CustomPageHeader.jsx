import React from 'react';
import { PageHeader, Button, Descriptions, Tag, Badge, Popover } from 'antd';
import { ApplicationContext } from '../../context/application.context';
import { DeviceContext } from '../../context/device.context';
import ChooseDevice from '../device/ChooseDevice';
import DeviceInfo from '../device/DeviceInfo';

class CustomPageHeader extends React.Component {

    getExtra(device)
    {
        if (!device)
        {
            return(
                [
                    <Badge status="error" text={<b>No device connected</b>} />,
                    <Popover placement="bottomRight" title={"Connect a device"} content={<div style={{width: 500}}><ChooseDevice /></div>} trigger="click">
                        <Button key="1" type="primary" size="small">connect</Button>
                    </Popover>
                ]
            )
        }

        return(
            [
                <Badge status="processing" text={<b>{device.serial} connected</b>} />,
                <Popover placement="bottomRight" title={"Connected Device Info"} content={<div style={{width: 700}}><DeviceInfo /></div>} trigger="click">
                    <Button key="1" type="primary" size="small">info</Button>
                </Popover>
            ]
        )
    }

    render()
    {
        return(
                <div className="custom-header">
                    <ApplicationContext.Consumer>
                        {context =>
                            <DeviceContext.Consumer>
                                {devContext =>
                                    <PageHeader
                                        className="custom-header"
                                        ghost={false}
                                        onBack={() => window.history.back()}
                                        title={context.application ? context.application.name : "No application selected"}
                                        subTitle={(context.application && context.application.valid_apk) ? <Tag color="success">valid APK</Tag> : <Tag color="error">non-valid APK</Tag>}
                                        extra={[this.getExtra(devContext.device)]}
                                        >
                                        <Descriptions size="small" column={3}>
                                            <Descriptions.Item label={<b>APK Id</b>}>{context.application ? context.application.application : "No application selected"}</Descriptions.Item>
                                            <Descriptions.Item label={<b>Package</b>}>{context.application ? context.application.package : "No application selected"}</Descriptions.Item>
                                            <Descriptions.Item label={<b>Version Name</b>}>{context.application ? context.application.version_name : "No application selected"}</Descriptions.Item>
                                            <Descriptions.Item label={<b>Version Code</b>}>{context.application ? context.application.version_code : "No application selected"}</Descriptions.Item>
                                            <Descriptions.Item label={<b>Target SDK Version</b>}>{context.application ? context.application.target_sdk_version : "No application selected"}</Descriptions.Item>
                                        </Descriptions>
                                    </PageHeader>
                                }
                            </DeviceContext.Consumer>

                        }
                    </ApplicationContext.Consumer>
                </div>
        );
    }
}

export default CustomPageHeader;