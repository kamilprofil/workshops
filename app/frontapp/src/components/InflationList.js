import React from 'react';
import axios from 'axios';

import  { Table } from 'antd';



export default class InflationList extends React.Component {
  state = {
    persons: []
  }
  
 columns = [
    {
        'title' :'Rok',
        key: 'rok',
        dataIndex: 'rok'

    },
    {
        'title' :'Miesiąc',
        key: 'miesiac',
        dataIndex: 'miesiac'

    },
    {
        'title' :'Wartość',
        key: 'wartosc',
        dataIndex: 'wartosc'

    }

  ]

  componentDidMount() {
    axios.get(process.env.REACT_APP_API_URL + "/items")
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