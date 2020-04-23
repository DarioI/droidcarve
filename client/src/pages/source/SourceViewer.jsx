import React from 'react';
import { Row, Col, Card, Tree, message} from 'antd';
import { sourceService } from '../../services/source.service';
import CodeWindow from '../../components/source/CodeWindow';

const { DirectoryTree } = Tree;

class SourceViewer extends React.Component {

    constructor(props) {
        super(props)
        this.state = {
            application: null,
            loadingTree: true,
            treeData: [],
            file: null,
            fileKey: null,
        }
        this.instance = null;
        this.getFile = this.getFile.bind(this);
    }

    componentDidMount()
    {
        sourceService.getSourceTree()
            .then(result => result.data)
            .then(data => {

                this.setState({treeData: data.children, loadingTree: false, fileKey: this.props.location.fileKey ? this.props.location.fileKey: null})
            })
            .catch(error => message.error("Could not load source tree."))
    }

    getFile(key)
    {
        this.setState({fileKey: key})
    }


    render()
    {
        const {application} = this.state;

        const onSelect = (keys, event) => {
            this.getFile(keys[0])
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
                            <CodeWindow fileKey={this.state.fileKey} />
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