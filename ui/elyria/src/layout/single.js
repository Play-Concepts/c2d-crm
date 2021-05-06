import React, {createRef} from "react";
import { Header } from "../components/header";

const SingleLayout = ({children}) => {
    const contextRef = createRef();
    return (
        <div ref={contextRef}>
            <Header context={contextRef} />
            <div>
                This is where you code your Layout
            </div>
            { children }
        </div>
    );
}
export default SingleLayout;