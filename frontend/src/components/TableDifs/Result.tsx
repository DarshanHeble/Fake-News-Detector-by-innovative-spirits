import style from './Result.module.css';
import React from 'react';

interface TableRow {
  source: string;
  link: string;
  result: string;
}

interface ResultsTableProps {
  data: TableRow[]; // Array of data to display
}

export class ResultsTable extends React.Component<ResultsTableProps> {
  render() {
    const { data } = this.props;

    return (
      <table className='tableContainer'>
        <thead>
          <tr>
            <th>Source</th>
            <th>Link</th>
            <th>Result</th>
          </tr>
          <tbody>
            {data.map((row, index) => (
              <tr key={index}>
                <td>{row.source}</td>
                <td>
                  <a href={row.link} target='_blank' rel='noreferrer'>
                    {row.link}
                  </a>
                </td>
                <td>{row.result}</td>
              </tr>
            ))}
          </tbody>
        </thead>
      </table>
    );
  }
}