import React from 'react';
import axios from 'axios';

import  { Table } from 'antd';

export default class InflationList extends React.Component {
  state = {
    persons: []
  }
  
 columns = [
    {
        'title' :'Id',
        key: 'id',
        dataIndex: 'id'

    },
    {
        'title' :'Name',
        key: 'name',
        dataIndex: 'name'

    }
  ]

  componentDidMount() {
    axios.get(`http://127.0.0.1:8000/items`)
      .then(res => {
        const persons = res.data;
        this.setState({ persons });
      })
  }

  render() {
    return (
          <Table columns={this.columns} dataSource={ this.state.persons } />
    )
  }
}