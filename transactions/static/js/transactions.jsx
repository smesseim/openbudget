var Transaction = React.createClass({
    render: function () {
        return (
            <tr className="transaction">
                <td className="col-md-1">
                    {this.props.id}
                </td>
                <td className="col-md-3">
                    {this.props.date}
                </td>
                <td className="col-md-3">
                    {this.props.payee}
                </td>
                <td className="col-md-3">
                    {this.props.memo}
                </td>
                <td className="col-md-2 text-right">
                    {this.props.delta}
                </td>
            </tr>
        )
    }
});

var TransactionList = React.createClass({
    render: function () {
        var transactionNodes = this.props.data.map(function (transaction) {
            return (
                <Transaction id={transaction.id} date={transaction.date}
                             payee={transaction.payee} memo={transaction.memo}
                             delta={transaction.delta} key={transaction.id}/>
            )
        });
        return (
            <table
                className="transactionList table table-striped table-bordered table-condensed">
                <thead>
                <tr>
                    <th>id</th>
                    <th>Date</th>
                    <th>Payee</th>
                    <th>Memo</th>
                    <th>Inflow/Outflow</th>
                </tr>
                </thead>
                <tbody>
                {transactionNodes}
                </tbody>
            </table>
        )
    }
});

var TransactionForm = React.createClass({
    getInitialState: function () {
        return {date: "", payee: "", memo: "", delta: ""};
    },
    handleDateChange: function (e) {
        this.setState({date: e.target.value});
    },
    handlePayeeChange: function (e) {
        this.setState({payee: e.target.value});
    },
    handleMemoChange: function (e) {
        this.setState({memo: e.target.value});
    },
    handleDeltaChange: function (e) {
        this.setState({delta: e.target.value});
    },
    handleSubmit: function (e) {
        e.preventDefault();
        var date = this.state.date.trim();
        var payee = this.state.payee.trim();
        var memo = this.state.memo.trim();
        var delta = this.state.delta.trim();
        if (!date || !delta) {
            return;
        }
        this.props.onTransactionSubmit({
            date: date,
            payee: payee,
            memo: memo,
            delta: delta
        });
        this.setState(this.getInitialState());
    },
    render: function () {
        return (
            <form className="transactionForm row" onSubmit={this.handleSubmit}>
                <input type="submit" value="Submit" className="col-md-1"/>
                <input type="date" placeholder="Date" value={this.state.date}
                       onChange={this.handleDateChange} className="col-md-3"/>
                <input type="text" placeholder="Payee" value={this.state.payee}
                       onChange={this.handlePayeeChange} className="col-md-3"/>
                <input type="text" placeholder="Memo" value={this.state.memo}
                       onChange={this.handleMemoChange} className="col-md-3"/>
                <input type="text" placeholder="Delta" value={this.state.delta}
                       step="0.01" onChange={this.handleDeltaChange}
                       className="col-md-2 text-right"/>
            </form>
        )
    }
});

var TransactionBox = React.createClass({
    loadCommentsFromServer: function () {
        $.ajax({
            url: this.props.url,
            dataType: "json",
            type: 'GET',
            cache: false,
            success: function (data) {
                this.setState({data: data});
            }.bind(this),
            error: function (xhr, status, err) {
                console.error(this.props.url, status, err.toString());
            }.bind(this)
        });
    },
    handleTransactionSubmit: function (transaction) {
        transaction.csrfmiddlewaretoken = csrf;
        $.ajax({
            url: this.props.url,
            dataType: 'json',
            type: 'POST',
            data: transaction,
            success: function (data) {
                this.setState({data: data});
            }.bind(this),
            error: function (xhr, status, err) {
                console.error(this.props.url, status, err.toString());
            }.bind(this)
        });
    },
    getInitialState: function () {
        return {data: []};
    },
    componentDidMount: function () {
        this.loadCommentsFromServer();
        setInterval(this.loadCommentsFromServer, this.props.pollInterval);
    },
    render: function () {
        return (
            <div className="transactionBox container">
                <TransactionList data={this.state.data}/>
                <TransactionForm
                    onTransactionSubmit={this.handleTransactionSubmit}/>
            </div>
        )
    }
});

ReactDOM.render(
    <TransactionBox url="/api/transactions/" pollInterval={2000}/>,
    document.getElementById("react-main")
);
