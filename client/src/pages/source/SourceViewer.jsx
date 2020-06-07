import React from 'react';
import { Row, Col, Card, Tree, message, Tabs} from 'antd';
import { sourceService } from '../../services/source.service';
import CodeWindow from '../../components/source/CodeWindow';

const { DirectoryTree } = Tree;
const { TabPane } = Tabs;

class SourceViewer extends React.Component {

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
        }
        this.instance = null;
        this.getFile = this.addFile.bind(this);
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
        sourceService.getSourceTree()
            .then(result => result.data)
            .then(data => {
                this.setState({
                    treeData: data.children,
                    loadingTree: false,
                    fileKey: this.props.location.fileKey ? this.props.location.fileKey: null,
                    lineNumber: this.props.location.lineNumber ? this.props.location.lineNumber : 1,
                    panes: panes,
                    activeKey: this.props.location.fileKey
                })
            })
            .catch(error => message.error("Could not load source tree."))
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
            content: <CodeWindow fileKey={key} />
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


    render()
    {
        const {application, panes, activeKey} = this.state;

        const onSelect = (keys, event) => {

            if (event.node.isLeaf)
            {
                this.addFile(keys[0], event.node.name)
            }
        };

        if (!application) {
            return(
                <Row gutter={[16, 24]}>
                    <Col span={6}>
                        <Card loading={this.state.loadingTree} title={"File Browser"} style={{minHeight: 600, overflow: 'scroll'}} extra={<a>Help</a>}>
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

export default SourceViewer;