import React from 'react';
import {Link} from 'react-router-dom';
import { Card, Table, message, Input } from 'antd';
import { appService } from '../../services';

const {Search} = Input;

class URLOverview extends React.Component {

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

    getData(urls)
    {
        if(!urls || Object.keys(urls) === 0)
        {
            return []
        }

        const data = []
        var i = 0

        urls.forEach(url => {
            data.push({
                key: i,
                name: <a target="_blank" rel="noopener noreferrer" href={url.url}>{url.url}</a>,
                class: url.class.name,
                class_key: url.class.key,
                class_ln: url.line_number
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
                    data: result.data.urls
                })
            })
            .catch(error => {
                message.error("Could not load APK.")
            })
    }

    render()
    {

        const columns = [
            {
              title: 'URL',
              dataIndex: 'name',
              key: 'name',
            },
            {
                title: 'Class',
                dataIndex: 'class',
                key: 'class',
                render: (text, record, index) => (
                  <span className="table-operation">
                        <Link to={{pathname: `${"/source"}`, fileName: record.class, fileKey: record.class_key, lineNumber: record.class_ln}}><span>{record.class}</span></Link>
                  </span>
                ),
              },
          ];
        return(
            <Card
                title="URLs"
                loading={this.state.loading}
                extra={
                        <Search
                        placeholder="Filter on url ..."
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
                />
            </Card>
        )
    }
}

export default URLOverview;