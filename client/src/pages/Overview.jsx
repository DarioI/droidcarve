import React from 'react';
import { Row, Col, message} from 'antd';
import { appService } from '../services';
import StatisticCard from '../components/dashboard/StatisticCard';

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
                console.log(data)
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

        const {crypto, urls, safetynet, dynamic} = this.state;

        return(
            <Row gutter={[16, 24]} type="browser">
                <Col className="gutter-row" span={12}>
                    <StatisticCard title="Cryptography" value={crypto ? crypto.length : 0} suffix={"crypto calls found"} deeplink={"/analysis/crypto"} />
                </Col>
                <Col className="gutter-row" span={12}>
                    <StatisticCard title="Dynamic Code Loading" value={dynamic ? dynamic.length : 0} suffix={"dynamic code loading calls found"} deeplink={"/analysis/dynamicloading"} />
                </Col>
                <Col className="gutter-row" span={12}>
                    <StatisticCard title="URLs" value={urls ? urls.length : 0} suffix={"URLs found"} deeplink={"/analysis/urls"} />
                </Col>
                <Col className="gutter-row" span={12}>
                    <StatisticCard title="SafetyNet" value={safetynet ? safetynet.length : 0} suffix={"SafetyNet calls found"} deeplink={"/analysis/safetynet"} />
                </Col>
            </Row>
        )
    }
}

export default Overview;