import React from 'react';
import APKUploader from '../components/upload/APKUploader';
import { Typography, Layout } from 'antd';
const { Title } = Typography;
const { Content, Footer } = Layout;

export class StartView extends React.Component {

    constructor(props)
    {
        super(props)

        this.onDone = this.onDone.bind(this);
    }

    onDone()
    {
        window.location.reload();
    }

    render()
    {
        return(
            <Layout className="site-layout" style={{height: '100vh'}}>
                <Content>
                    <div style={{padding: 100, textAlign: 'center'}}>
                        <Title level={4}>Start by selecting an APK for analysis</Title>
                        <APKUploader onDone={this.onDone}/>
                    </div>
                </Content>
                <Footer style={{ textAlign: 'center' }}>DroidCarve ©2020 Created by Dario Incalza - dario.incalza@gmail.com </Footer>
            </Layout>
        )
    }
}