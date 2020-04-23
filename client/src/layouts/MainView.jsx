import React from 'react';

import { Layout, Menu} from 'antd';

import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link,
    Redirect
  } from "react-router-dom";


import routes from "../routes/routes";
import CustomPageHeader from '../components/layout/CustomPageHeader';

const { SubMenu } = Menu;
const { Content, Sider, Footer } = Layout;

var Url = require('url-parse');

export class MainView extends React.Component {

    constructor(props)
    {
        super(props)

        this.state = {
            collapsed: false,
        };

        this.onCollapse = this.onCollapse.bind(this);
    }

    onCollapse = collapsed => {
        this.setState({ collapsed });
    };

    activeRoute() {
        var url = new Url(window.location.href).pathname;
        url = url.substring(1, url.length);
        for (var key in routes)
        {
          if (url.indexOf(routes[key].path) > -1 )
          {
            return [key]
          }
        }
    }

    render(){

        return(
            <Router>
            <Layout style={{ minHeight: '100vh' }}>
                <Sider collapsible collapsed={this.state.collapsed} onCollapse={this.onCollapse}>
                <div className="logo">{this.state.collapsed ? "DC" : "DroidCarve"}</div>
                <Menu theme="dark" defaultSelectedKeys={this.activeRoute()} mode="inline">
                    {routes.map((prop, key) => {
                        if(prop.visible) {
                            if (!prop.sub)
                            {
                                return(
                                    <Menu.Item key={key}>
                                        {prop.icon}
                                        <span>{prop.name}</span>
                                        <Link to={prop.path}></Link>
                                    </Menu.Item>
                                )

                            }else{
                                return(
                                    <SubMenu
                                        key={key}
                                        title={
                                            <span>
                                            {prop.icon}
                                            <span>{prop.name}</span>
                                            </span>
                                        }
                                    >
                                    {prop.sub.map((prop2, key2) => {
                                        return(<Menu.Item key={"sub"+key2}>{prop2.name}<Link to={prop2.path}></Link></Menu.Item>)
                                    })}
                                </SubMenu>
                                )
                            }
                        }else {return(null)}
                    })}
                </Menu>
                </Sider>
                <Layout className="site-layout">
                    <CustomPageHeader />
                    <Content style={{ margin: '0 16px' }}>
                        <div style={{ margin: '16px 0', padding: 24, minHeight: 360 }}>
                        <Switch>
                            {routes.map((prop, key) => {
                            if (prop.sub) {
                            return prop.sub.map((prop2, key2) => {
                                return (
                                <Route
                                    path={prop2.path}
                                    component={prop2.component}
                                    key={key2}
                                />
                                );
                            });
                            }
                            if (prop.redirect)
                            return <Redirect from={prop.path} to={prop.pathTo} key={key} />;
                            return (
                                <Route path={prop.path} component={prop.component} key={key} />
                            );
                        })}

                        </Switch>
                        </div>
                    </Content>
                    <Footer style={{ textAlign: 'center' }}>DroidCarve ©2020 Created by Dario Incalza - dario.incalza@gmail.com </Footer>
                </Layout>
            </Layout>
            </Router>
        )

    }
}