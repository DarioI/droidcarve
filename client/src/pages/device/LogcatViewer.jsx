import React from 'react';
import { Row, Col, Card, Button, message} from 'antd';
import { deviceService } from '../../services';


class SourceViewer extends React.Component {

    componentDidMount()
    {
    }

    startAdb()
    {
        deviceService.startLogcat()
            .then(result => {
                console.log(result)
            })
            .catch(error => {
                message.error('Could not start logcat.')
            })
    }


    render()
    {

        return(
            <Row gutter={[16, 24]}>
                <Col span={6}>
                    <Card title={"LogCat"} style={{minHeight: 600, overflow: 'scroll'}} extra={<a>Help</a>}>
                        <Button type="primary" onClick={this.startAdb}>Start LogCat</Button>
                    </Card>
                </Col>
            </Row>
        )
    }
}

export default SourceViewer;