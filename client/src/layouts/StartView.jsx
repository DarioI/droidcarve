import React from 'react';
import APKUploader from '../components/upload/APKUploader';
import { Typography, Layout, Tabs } from 'antd';
import { ApiOutlined, AndroidOutlined } from '@ant-design/icons';
import ChooseAPK from '../components/device/ChooseAPK';

const { Title } = Typography;
const { Content, Footer } = Layout;
const { TabPane } = Tabs;

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
                    <Tabs defaultActiveKey="1">
                            <TabPane
                            tab={
                                <span>
                                <AndroidOutlined />
                                Start from APK
                                </span>
                            }
                            key="1"
                            >
                            <APKUploader onDone={this.onDone}/>
                            </TabPane>
                            <TabPane
                            tab={
                                <span>
                                <ApiOutlined />
                                Dump from device
                                </span>
                            }
                            key="2"
                            >
                                <ChooseAPK />
                            </TabPane>
                        </Tabs>
                    </div>
                </Content>
                <Footer style={{ textAlign: 'center' }}>DroidCarve ©2020 Created by Dario Incalza - dario.incalza@gmail.com </Footer>
            </Layout>
        )
    }
}