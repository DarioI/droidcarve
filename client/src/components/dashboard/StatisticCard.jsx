import React from 'react';
import {Link} from 'react-router-dom';
import {Statistic, Card} from 'antd';

class StatisticCard extends React.Component {

    render()
    {
        return(
            <Link to={this.props.deeplink}>
                <Card>
                    <Statistic
                        title={this.props.title}
                        value={this.props.value}
                        valueStyle={{ color: this.props.value > 0 ? '#cf1322' : '#3f8600' }}
                        suffix={this.props.suffix}
                    />
                </Card>
            </Link>
        )
    }
}

export default StatisticCard;