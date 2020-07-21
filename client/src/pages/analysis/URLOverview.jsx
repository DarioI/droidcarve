import React from 'react';
import {Link} from 'react-router-dom';
import { Card, Table, message, Input, Drawer, Button } from 'antd';
import { appService } from '../../services';
import CodeWindow from '../../components/source/CodeWindow';

const {Search} = Input;

class URLOverview extends React.Component {

    constructor(props)
    {
        super(props)
        this.state = {
            loading: true,
            tableData: [],
            origData: [],
            filter: null,
            quickCode: {
                visible: false,
                fileKey: null,
                lineNumber: null,
                fileName: null
            }
        }

        this.getData = this.getData.bind(this)
        this.closeQuickCodePanel = this.closeQuickCodePanel.bind(this)
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

    closeQuickCodePanel()
    {
        this.setState({
            quickCode: {
                visible: false,
                fileKey: null,
                fileName: null,
                lineNumber: null,
            }
        })
    }

    showQuickCodePanel(fileKey, fileName, lineNumber)
    {
        this.setState({
            quickCode: {
                visible: true,
                fileKey,
                fileName,
                lineNumber
            }
        })
    }

    componentDidMount()
    {

        appService.getAnalysisOverview()
            .then(result => {
                this.setState({
                    loading: false,
                    origData: result.data.urls,
                    tableData: result.data.urls
                })
            })
            .catch(error => {
                message.error("Could not load APK.")
            })
    }

    filterURLs(query)
    {

        var filtered = this.state.origData.filter(url => {
            return (url.url.includes(query))
        })

        this.setState({
            tableData: filtered
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
                       <Button size="small" onClick={()=>this.showQuickCodePanel(record.class_key, record.class, record.class_ln)}>{record.class}</Button>
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
                        onChange={e => this.filterURLs(e.target.value)}
                        onSearch={value => this.filterURLs(value)}
                        style={{ width: 400 }}
                    />}
            >
               <Table
                loading={this.state.loading}
                showHeader={false}
                dataSource={this.getData(this.state.tableData)}
                columns={columns}
                pagination={{"hideOnSinglePage": true}}
                size={"small"}
                />
                <Drawer
                    title={this.state.quickCode.fileName}
                    placement={"right"}
                    closable={true}
                    width={"50%"}
                    onClose={this.closeQuickCodePanel}
                    visible={this.state.quickCode.visible}
                    key={"drawer"}
                    >
                    <CodeWindow fileKey={this.state.quickCode.fileKey} />
                </Drawer>
            </Card>
        )
    }
}

export default URLOverview;