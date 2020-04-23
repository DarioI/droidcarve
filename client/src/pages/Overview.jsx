import React from 'react';
import { Row, Col, Card, Badge, message} from 'antd';
import { appService } from '../services';
import CryptoInfo from '../components/CryptoInfo';

class Overview extends React.Component {

    constructor(props)
    {
        super(props)
        this.state = {
            loading: true,
            classes: null,
            crypto: null,
            urls: null,
            safetynet: null,
            dynamic: null,
        }
    }

    componentDidMount()
    {
        appService.getAnalysisOverview()
            .then(result => result.data)
            .then(data => {
                this.setState({
                        loading: false,
                        crypto: data.crypto,
                        classes: data.classes,
                        urls: data.urls,
                        safetynet: data.safetynet,
                        dynamic: data.dynamic,
                    })
            })
            .catch(error => {
                this.setState({loading: false})
                message.error("Could not load analysis overview.")
            })
    }

    render()
    {

        const {loading, crypto, urls, safetynet, dynamic} = this.state;

        return(
            <Row gutter={[16, 24]} type="browser">
                <Col className="gutter-row" span={12}>
                        <CryptoInfo crypto={crypto} loading={loading}/>
                </Col>
                <Col className="gutter-row" span={12}>
                        <Card title="Dynamic Code Loading" loading={loading} extra={<Badge overflowCount={1000000} count={dynamic ? Object.keys(dynamic).length: 0}/>}>
                            {dynamic && dynamic.length > 0 &&
                                <p>{dynamic.length} dynamic code loading calls found.</p>
                            }
                            {(!dynamic || dynamic.length === 0) &&
                                <p>No dynamic code loading calls found.</p>
                            }
                        </Card>
                </Col>
                <Col className="gutter-row" span={12}>
                        <Card title="URL" loading={loading} extra={<Badge overflowCount={1000000} count={urls ? urls.length: 0}/>}>
                            {urls && urls.length > 0 &&
                                <p>{urls.length} URLs found.</p>
                            }
                            {(!urls || urls.length === 0) &&
                                <p>No URLs found.</p>
                            }
                        </Card>
                </Col>
                <Col className="gutter-row" span={12}>
                        <Card title="SafetyNet" loading={loading} extra={<Badge overflowCount={1000000} count={safetynet ? Object.keys(safetynet).length: 0}/>}>
                            {safetynet && safetynet.length > 0 &&
                                <p>{safetynet.length} SafetyNet calls found.</p>
                            }
                            {(!urls || urls.length === 0) &&
                                <p>No SafetyNet calls found.</p>
                            }
                        </Card>
                </Col>
            </Row>
        )
    }
}

export default Overview;