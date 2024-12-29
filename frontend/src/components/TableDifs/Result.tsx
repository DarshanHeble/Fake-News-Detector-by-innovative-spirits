// /GitHub/Fake-News-Detection-testing/frontend/src/components/TableDifs/Result.tsx
import React from 'react';
import style from './Result.module.css';

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
      <div className={style.tableContainer}>
        {data.length > 0 ? (
          <table className={style.table}>
            <thead>
              <tr>
                <th>Source</th>
                <th>Article</th>
                <th>Result</th>
              </tr>
            </thead>
            <tbody>
              {data.map((item, index) => (
                <tr key={index}>
                  <td>{item.source}</td>
                  <td>
                    <a href={item.link} target="_blank" rel="noreferrer">
                      Click here
                    </a>
                  </td>
                  <td>
                    <span className={item.result === "fake" ? style.red : style.green}>
                      {item.result}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p>No data available.</p>
        )}
      </div>
    );
  }
}