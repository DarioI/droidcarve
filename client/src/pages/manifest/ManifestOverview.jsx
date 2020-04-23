import React from 'react';

import {Row, Col, Tabs, message, Card, List, Badge} from 'antd';
import {ManifestCodeWindow, IntentFilterOverviewTable, SearchableOverviewTable} from '../../components/manifest/';
import { manifestService } from '../../services';

const { TabPane } = Tabs;

class ManifestOverview extends React.Component {

    constructor(props) {
        super(props)
        this.state = {
            manifest: null,
            data: null,
            loading: true,
        }
    }

    componentDidMount()
    {
        manifestService.getOverview()
            .then(result => result.data)
            .then(data => {
                this.setState({data: data, loading: false})
            })
            .catch(error => {
                message.error("Could not load AndroidManifest.xml information.");
            })
    }


    render()
    {
        const {data, loading} = this.state;

        return(
            <Row>
                    <Col span={24}>
                        <Tabs defaultActiveKey="1">
                            <TabPane tab="XML" key="1">
                                <ManifestCodeWindow />
                            </TabPane>
                            <TabPane tab={data ? <Badge count={data.activities.length} offset={[8,0]}><span>Activities</span></Badge>: "Activities"} key="2">
                                <Card loading={loading}>
                                    {data && <IntentFilterOverviewTable elements={data.activities} />}
                                </Card>
                            </TabPane>
                            <TabPane tab={data ? <Badge count={data.permissions.length} offset={[8,0]}><span>Permissions</span></Badge>: "Permissions"} key="3">
                                <Card loading={loading}>
                                    {data && <SearchableOverviewTable elements={data.permissions} />}
                                </Card>
                            </TabPane>
                            <TabPane tab={data ? <Badge count={data.features.length} offset={[8,0]}><span>Features</span></Badge>: "Features"} key="4">
                                <Card loading={loading}>
                                    {data && <SearchableOverviewTable elements={data.features} />}
                                </Card>
                            </TabPane>
                            <TabPane tab={data ? <Badge count={data.services.length} offset={[8,0]}><span>Services</span></Badge>: "Services"} key="5">
                                <Card loading={loading}>
                                    {data && <IntentFilterOverviewTable elements={data.services} />}
                                </Card>
                            </TabPane>
                            <TabPane tab={data ? <Badge count={data.providers.length} offset={[8,0]}><span>Providers</span></Badge>: "Providers"} key="6">
                                <Card loading={loading}>
                                    {data && <IntentFilterOverviewTable elements={data.providers} />}
                                </Card>
                            </TabPane>
                        </Tabs>
                    </Col>
                </Row>
        )
    }
}

export default ManifestOverview;