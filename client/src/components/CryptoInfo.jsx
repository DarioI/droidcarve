import React from 'react';
import { Card, Table, Badge } from 'antd';
import { Link } from "react-router-dom";
import { smaliClassToJava, isAndroidPackage, javaPackageToAndroidAPIUrl } from '../utils/android.utils';


class CryptoInfo extends React.Component {

    constructor(props)
    {
        super(props)
        this.state = {
            data: null
        }

        this.getData = this.getData.bind(this)
    }

    getData(crypto)
    {
        if(!crypto || Object.keys(crypto) === 0)
        {
            return []
        }

        const data = []
        var i = 0
        Object.keys(crypto).forEach(call => {
            const javaPkgName = smaliClassToJava(call);
            const isAndroidCall = isAndroidPackage(javaPkgName);
            data.push({
                key: i,
                call: call,
                name: (isAndroidCall) ? <a target="_blank" rel="noopener noreferrer" href={javaPackageToAndroidAPIUrl(javaPkgName)}>{javaPkgName}</a> : javaPkgName,
                count: <Badge count={crypto[call].length} />
            })
            i++;
        })

        return data
    }

    render()
    {
        const columns = [
            {
              title: 'API Call',
              dataIndex: 'name',
              key: 'name',
            },
            {
              title: 'Count',
              dataIndex: 'count',
              key: 'count',
            }
          ];
        return(
            <Card title="Cryptography" loading={this.props.loading} extra={<Link to={"/analysis/crypto"}>View more</Link>}>
               <Table
                showHeader={false}
                dataSource={this.getData(this.props.crypto)}
                columns={columns}
                pagination={{"hideOnSinglePage": true}}
                size={"small"}
                />
            </Card>
        )
    }
}

export default CryptoInfo;