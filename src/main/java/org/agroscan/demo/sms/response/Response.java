package org.agroscan.demo.sms.response;

public class Response {
    private DataResponse data;
    private String message;
    private String error;

    public DataResponse getData() {
        return data;
    }

    public void setData(DataResponse data) {
        this.data = data;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public String getError() {
        return error;
    }

    public void setError(String error) {
        this.error = error;
    }

    @Override
    public String toString() {
        return "Response{" +
                "data=" + data +
                ", message='" + message + '\'' +
                '}';
    }
}

