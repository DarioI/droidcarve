import React from 'react';
import { message, Button, Card, Table, Input } from 'antd';
import { DownloadOutlined } from '@ant-design/icons';
import { deviceService } from '../../services';
import Loader from 'react-loader-spinner'

import "react-loader-spinner/dist/loader/css/react-spinner-loader.css"
import { Route } from 'react-router-dom'

const { Search } = Input;

const DoneButton = () => (
    <Route render={({ history }) => (
      <Button type="primary" onClick={() => history.push("/")}>View results</Button>
    )} />
  )

class APKDownloader extends React.Component {

    constructor(props)
    {
        super(props)
        this.state = {
            loading: true,
            packages: [],
            origPackages: [],
            analyzing: false,
            analyzed: false,
            selected_pckg: null,
        }

        this.refresh = this.refresh.bind(this);
        this.filterPackages = this.filterPackages.bind(this);
    }

    componentDidMount()
    {
        this.refresh()
    }

    refresh()
    {
        this.setState({loading: true})
        deviceService.getPackages()
            .then(result => result.data)
            .then(data => {
                var packages = data.map(item => {
                    return {
                        key: item,
                        name: item
                    }
                })
               this.setState({loading: false, packages: packages, origPackages: packages})
            })
            .catch(error => {
                this.setState({loading: false})
                message.error("Could not load packages.")
            })
    }

    filterPackages(query)
    {
        var filtered = this.state.origPackages.filter(item => {
            if (item.name.includes(query)) return item;
        })
        if (query === "")
        {
            this.setState({packages: this.state.origPackages})
        }else{
            this.setState({packages: filtered})
        }
    }

    onClickAPK(record)
    {
        this.setState({loading: true, analyzing: true, selected_pckg: record.name})
        deviceService.dumpAnalyze(record.name)
            .then(result => {
                console.log(result.data)
                window.location.reload();
            })
            .catch(error => {
                message.error("Something went wrong while dumping and analyzing the APK.")
                this.setState({loading: false})
            })
    }


    render()
    {

        if (this.state.analyzing)
        {
            return(
                <Card title={`Analyzing ${this.state.selected_pckg}`}>
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
                </Card>
            )
        }

        const columns = [
            { title: 'Package', dataIndex: 'name', key: 'name' },
            {
              title: 'Action',
              dataIndex: '',
              key: 'x',
              render: (text, record, index) => <Button style={{float: 'right'}} key={record} type="primary" size="small" onClick={() => this.onClickAPK(record)} icon={<DownloadOutlined />}>analyze</Button>,
            },
          ];

        return(
                <Card title={`Found ${this.state.packages.length} packages installed`} extra={<Search
                    placeholder="Search packages"
                    onSearch={value => this.filterPackages(value)}
                    style={{ width: 200 }}
                  />}>
                     <Table
                        loading={this.state.loading}
                        columns={columns}
                        pagination={{ pageSize: 5 }}
                        dataSource={this.state.packages}
                    />
                </Card>
        )
    }
}

export default APKDownloader;