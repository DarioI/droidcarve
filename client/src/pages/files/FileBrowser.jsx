import React from 'react';
import { Row, Col, Card, Tree, message, Tabs, Input} from 'antd';
import { fileService } from '../../services/file.service';
import CodeWindow from '../../components/source/CodeWindow';

const { DirectoryTree } = Tree;
const { TabPane } = Tabs;
const { Search } = Input;

class FileBrowser extends React.Component {

    constructor(props) {
        super(props)
        this.state = {
            application: null,
            loadingTree: true,
            treeData: [],
            file: null,
            fileKey: null,
            openFiles: [],
            activeKey: null,
            panes: [],
            expandedKeys: [],
            searchValue: '',
            autoExpandParent: true,
        }
        this.instance = null;
        this.getFile = this.addFile.bind(this);
        this.searchTree = this.searchTree.bind(this);
    }

    componentDidMount()
    {
        var panes = []

        if (this.props.location.fileKey)
        {
            panes.push({
                key: this.props.location.fileKey,
                title: this.props.location.fileName ? this.props.location.fileName : 'filename.smali',
                content: <CodeWindow fileKey={this.props.location.fileKey} />
            })
        }

        fileService.getFileTree()
            .then(result => result.data)
            .then(data => {
                this.setState({
                    treeData: data.children,
                    filteredData: data.children,
                    loadingTree: false,
                    fileKey: this.props.location.fileKey ? this.props.location.fileKey: null,
                    lineNumber: this.props.location.lineNumber ? this.props.location.lineNumber : 1,
                    panes: panes,
                    activeKey: this.props.location.fileKey
                })
            })
            .catch(error => message.error("Could not load file tree."))
    }

    onChange = activeKey => {
        this.setState({ activeKey });
    };

    addFile(key, filename)
    {
        var panes = this.state.panes
        panes.push({
            key: key,
            title: filename,
            content: <CodeWindow fileKey={key} filename={filename}/>
        })
        this.setState({activeKey: key, panes: panes})
    }

    onEdit = (targetKey, action) => {
        this[action](targetKey);
    };

    remove = targetKey => {
        const { panes, activeKey } = this.state;
        let newActiveKey = activeKey;
        let lastIndex;
        panes.forEach((pane, i) => {
          if (pane.key === targetKey) {
            lastIndex = i - 1;
          }
        });
        const newPanes = panes.filter(pane => pane.key !== targetKey);
        if (newPanes.length && newActiveKey === targetKey) {
          if (lastIndex >= 0) {
            newActiveKey = newPanes[lastIndex].key;
          } else {
            newActiveKey = newPanes[0].key;
          }
        }
        this.setState({
          panes: newPanes,
          activeKey: newActiveKey,
        });
      };

    getParentKey = (key, tree) => {
        let parentKey;
        for (let i = 0; i < tree.length; i++) {
          const node = tree[i];
          if (node.children) {
            if (node.children.some(item => item.key === key)) {
              parentKey = node.key;
            } else if (this.getParentKey(key, node.children)) {
              parentKey = this.getParentKey(key, node.children);
            }
          }
        }
        return parentKey;
    };

    searchTree = e => {
        const { value } = e.target;
        const expandedKeys = this.state.treeData
          .map(item => {
            if (item.title.indexOf(value) > -1) {
              return this.getParentKey(item.key, this.state.treeData);
            }
            return null;
          })
          .filter((item, i, self) => item && self.indexOf(item) === i);
        this.setState({
          expandedKeys,
          searchValue: value,
          autoExpandParent: true,
        });
    };

    render()
    {
        const {application, panes, activeKey, searchValue, expandedKeys} = this.state;

        const onSelect = (keys, event) => {

            if (event.node.isLeaf)
            {
                this.addFile(keys[0], event.node.name)
            }
        };

        const loop = data =>
            data.map(item => {
                const index = item.title.indexOf(searchValue);
                const beforeStr = item.title.substr(0, index);
                const afterStr = item.title.substr(index + searchValue.length);
                const title =
                index > -1 ? (
                    <span>
                    {beforeStr}
                    <span className="site-tree-search-value">{searchValue}</span>
                    {afterStr}
                    </span>
                ) : (
                    <span>{item.title}</span>
                );
                if (item.children) {
                return { title, key: item.key, children: loop(item.children) };
                }

                return {
                title,
                key: item.key,
                };
        });

        if (!application) {
            return(
                <Row gutter={[16, 24]}>
                    <Col span={6}>
                        <Card loading={this.state.loadingTree} title={"File Browser"} style={{minHeight: 600, overflow: 'scroll'}} extra={<Search style={{ marginBottom: 8 }} placeholder="Search files" onChange={this.searchTree} />}>
                            <DirectoryTree
                                multiple
                                height={600}
                                showLine={false}
                                defaultExpandedKeys={this.props.location.fileKey ? [this.props.location.fileKey] : []}
                                defaultSelectedKeys={this.props.location.fileKey ? [this.props.location.fileKey] : []}
                                onSelect={onSelect}
                                treeData={this.state.treeData}
                            />
                        </Card>
                    </Col>
                    <Col span={18}>
                        <Card title={"Code"} style={{minHeight: 600, overflow: 'scroll'}} extra={<a>Help</a>}>
                            <Tabs
                                type="editable-card"
                                hideAdd
                                onChange={this.onChange}
                                activeKey={activeKey}
                                onEdit={this.onEdit}
                            >
                                {panes.map(pane => (
                                <TabPane tab={pane.title} key={pane.key} closable={pane.closable}>
                                    {pane.content}
                                </TabPane>
                                ))}
                            </Tabs>
                        </Card>
                    </Col>
                </Row>

            )
        }

        return(
            <p>Analysis</p>
        )
    }
}

export default FileBrowser;