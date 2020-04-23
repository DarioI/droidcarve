import React from 'react';
import { Link } from 'react-router-dom';
import { Card, Table, Badge, Input, Button, message } from 'antd';
import { smaliClassToJava, isAndroidPackage, javaPackageToAndroidAPIUrl } from '../../utils/android.utils';
import { appService } from '../../services';

const {Search} = Input;

class CryptoOverview extends React.Component {

    constructor(props)
    {
        super(props)
        this.state = {
            loading: true,
            data: [],
            filter: null
        }

        this.getData = this.getData.bind(this)
    }

    getData(crypto)
    {
        if(!crypto || Object.keys(crypto) === 0)
        {
            return []
        }

        const data = []
        var i = 0
        Object.keys(crypto).forEach(call => {
            const javaPkgName = smaliClassToJava(call);
            const isAndroidCall = isAndroidPackage(javaPkgName);
            data.push({
                key: i,
                call: call,
                crypto: crypto[call],
                name: (isAndroidCall) ? <a target="_blank" rel="noopener noreferrer" href={javaPackageToAndroidAPIUrl(javaPkgName)}>{javaPkgName}</a> : javaPkgName,
                count: <Badge count={crypto[call].length} />
            })
            i++;
        })

        return data
    }

    componentDidMount()
    {

        appService.getAnalysisOverview()
            .then(result => {
                this.setState({
                    loading: false,
                    data: result.data.crypto
                })
            })
            .catch(error => {
                message.error("Could not load APK.")
            })
    }

    render()
    {
        const expandedRowRender = (record) => {
            const columns = [
              { title: 'Class', dataIndex: 'class', key: 'class' },
              { title: 'Count', dataIndex: 'count', key: 'count' },
              {
                title: 'Action',
                dataIndex: 'operation',
                key: 'operation',
                render: (text, record, index) => (
                  <span className="table-operation">
                        <Link to={{pathname: `${"/source"}`, fileKey: record.key}}><Button type="primary" size="small">Source</Button></Link>
                  </span>
                ),
              },
            ];

            const data = [];
            const crypto = this.state.data;
            if (!crypto) { return <Table columns={columns} dataSource={data} pagination={false} />; }

            const classes = crypto[record.call];
            for (var i in classes)
            {
                const cleanName = smaliClassToJava(classes[i].name.replace(/\r?\n|\r/g, ""))
                const contains = data.filter(function(value) { return value.class === cleanName }).length !== 0;
                if (!contains) { data.push({ class: cleanName, key: classes[i].key, count: 1 }) }
                else{ for (var j in data) { if (data[j].class === cleanName) { data[j].count = data[j].count+1; } } }
            }


            return <Table columns={columns} dataSource={data} pagination={false} />;
        };

        const columns = [
            {
              title: 'API Call',
              dataIndex: 'name',
              key: 'name',
            },
            {
              title: 'Count',
              dataIndex: 'count',
              key: 'count',
            }
          ];
        return(
            <Card
                title="Cryptography"
                loading={this.state.loading}
                extra={
                        <Search
                        placeholder="Filter on classname ..."
                        onChange={e => console.log(e.target.value)}
                        onSearch={value => console.log(value)}
                        style={{ width: 400 }}
                    />}
            >
               <Table
                loading={this.state.loading}
                showHeader={false}
                dataSource={this.getData(this.state.data)}
                columns={columns}
                pagination={{"hideOnSinglePage": true}}
                size={"small"}
                expandable={{ expandedRowRender: record => expandedRowRender(record) }}
                />
            </Card>
        )
    }
}

export default CryptoOverview;