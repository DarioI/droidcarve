import React from 'react';

import {Table, Tag, Input, Button} from 'antd';
import Highlighter from 'react-highlight-words';
import { SearchOutlined } from '@ant-design/icons'


export class IntentFilterOverviewTable extends React.Component {

    constructor(props) {
        super(props)
        this.state = {
            elements: this.proces(this.props.elements),
            searchText: '',
            searchedColumn: '',
        }
    }

    componentWillReceiveProps(newProps)
    {

        this.setState({elements: this.proces(newProps.elements)})
    }

    proces(elements)
    {
        const data = []
        elements.forEach(a => {
            data.push({
                key: a.name,
                name: a.name ,
                actions: a.intent ? a.intent.action : [],
                categories: a.intent ? a.intent.category: [],
                exported: a.hasOwnProperty('exported') && (a.exported === 'true') ? true : false
            })
        })

        return data
    }

    handleSearch = (selectedKeys, confirm, dataIndex) => {
        confirm();
        this.setState({
          searchText: selectedKeys[0],
          searchedColumn: dataIndex,
        });
    };

    handleReset = clearFilters => {
        clearFilters();
        this.setState({ searchText: '' });
    };

    getColumnSearchProps = dataIndex => ({
        filterDropdown: ({ setSelectedKeys, selectedKeys, confirm, clearFilters }) => (
          <div style={{ padding: 8 }}>
            <Input
              ref={node => {
                this.searchInput = node;
              }}
              placeholder={`Search ${dataIndex}`}
              value={selectedKeys[0]}
              onChange={e => setSelectedKeys(e.target.value ? [e.target.value] : [])}
              onPressEnter={() => this.handleSearch(selectedKeys, confirm, dataIndex)}
              style={{ width: 188, marginBottom: 8, display: 'block' }}
            />
            <Button
              type="primary"
              onClick={() => this.handleSearch(selectedKeys, confirm, dataIndex)}
              icon={<SearchOutlined />}
              size="small"
              style={{ width: 90, marginRight: 8 }}
            >
              Search
            </Button>
            <Button onClick={() => this.handleReset(clearFilters)} size="small" style={{ width: 90 }}>
              Reset
            </Button>
          </div>
        ),
        filterIcon: filtered => <SearchOutlined style={{ color: filtered ? '#1890ff' : 'geekblue' }} />,
        onFilter: (value, record) =>
          record[dataIndex]
            .toString()
            .toLowerCase()
            .includes(value.toLowerCase()),
        onFilterDropdownVisibleChange: visible => {
          if (visible) {
            setTimeout(() => this.searchInput.select());
          }
        },
        render: (text, record) =>
          this.state.searchedColumn === dataIndex ? (
            <Highlighter
              highlightStyle={{ backgroundColor: '#ffc069', padding: 0 }}
              searchWords={[this.state.searchText]}
              autoEscape
              textToHighlight={text.toString()}
            />
          ) : (
              <div><b>{record.name}</b>{record.exported && <Tag color="red">exported</Tag>}</div>
          ),
      });


    render()
    {
        const columns = [
            {
              title: 'Name',
              dataIndex: 'name',
              key: 'name',
              render: record => {

                return(<div><b>{record.exported}</b>{record.exported && <Tag>exported</Tag>}</div>)
              },
              ...this.getColumnSearchProps('name'),
            },
            {
              title: 'Intent Action',
              key: 'actions',
              dataIndex: 'actions',
              render: actions => (
                <span>
                    {actions.map(action => (
                        <Tag color="blue" size="small" key={action}>
                            {action}
                        </Tag>
                    ))}
                </span>
              ),
            },
            {
              title: 'Intent Category',
              key: 'categories',
              dataIndex: 'categories',
              render: categories => (
                <span>
                    {categories.map(c => (
                        <Tag color="purple" size="small" key={c}>
                            {c}
                        </Tag>
                    ))}
                </span>
              ),
            }
          ];

        return(
            <Table columns={columns} dataSource={this.state.elements} scroll={{ x: 1300 }}/>
        )
    }
}