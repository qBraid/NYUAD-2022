import React from "react";
import { styled } from "buttered";

import AceEditor from "react-ace";

import "ace-builds/src-noconflict/mode-python";
import "ace-builds/src-noconflict/mode-html";
import "ace-builds/src-noconflict/mode-css";
import "ace-builds/src-noconflict/theme-monokai";

let Wrapper = styled('div')`
  #editor {
    width: 50vw!important;
    min-height: 66.667vh!important;
  }
`;

export let Editor = ({ onChange, value }) => {
  return (
    <Wrapper>
      <AceEditor
        mode="python"
        theme="monokai"
        value={value}
        onChange={onChange}
        name="editor"
        editorProps={{ $blockScrolling: true }}
      />
    </Wrapper>
  )
}