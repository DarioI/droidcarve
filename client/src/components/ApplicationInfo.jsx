import React from 'react';
import { Card, Table, Tag } from 'antd';
import { appService } from '../services';

class ApplicationInfo extends React.Component {

    constructor(props)
    {
        super(props)
        this.state = {
            loading: true,
            application: null
        }
    }

    componentDidMount()
    {
        appService.getCurrentApplication()
            .then(result => result.data)
            .then(data => {
                const appInfo = []
                appInfo.push({
                    key: '1',
                    name: <b>Name</b>,
                    value: data.name,
                  })
                appInfo.push({
                    key: '2',
                    name: <b>Package</b>,
                    value: data.package,
                  })
                appInfo.push({
                    key: '3',
                    name: <b>Valid APK</b>,
                    value: data.valid_apk ? <Tag color="success">valid</Tag>: <Tag color="error">not valid</Tag>,
                  })
                appInfo.push({
                    key: '4',
                    name: <b>Max SDK</b>,
                    value: data.max_sdk_version,
                  })
                appInfo.push({
                    key: '5',
                    name: <b>Min SDK</b>,
                    value: data.min_sdk_version,
                  })
                appInfo.push({
                    key: '6',
                    name: <b>Version</b>,
                    value: data.version_code,
                  })

                this.setState({
                    loading: false,
                    application: appInfo
                })
            })
    }

    render()
    {
        const {application, loading} = this.state;

        const columns = [
            {
              title: 'Name',
              dataIndex: 'name',
              key: 'name',
            },
            {
              title: 'Value',
              dataIndex: 'value',
              key: 'value',
            }
          ];
        return(
            <Card title="Application Info" loading={loading}>
               <Table showHeader={false} dataSource={application} columns={columns} pagination={{"hideOnSinglePage": true}} size={"small"} />
            </Card>
        )
    }
}

export default ApplicationInfo;