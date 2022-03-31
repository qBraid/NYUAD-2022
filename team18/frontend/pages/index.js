import { styled } from 'buttered';
import { Button, Textarea } from '@vapor/ui';
import { ArrowRight } from 'react-feather';

let Wrapper = styled('div')`
  display: grid;
  grid-template-columns: 1fr 1fr;

  @media screen and (max-width: 800px) {
    grid-template-columns: 1fr;
  }
`;

let LeftWrapper = styled('div')`
  min-height: 100vh;
  border-right: 1px solid var(--vapor-accent-9);
`;

let RightWrapper = styled('div')`
  display: grid;
  grid-template-rows: 1fr 1fr 1fr;
`;

let EditorWrapper = styled('div')`
  min-height: 100vh;
  background: var(--vapor-background);
  padding: 20px 20px;
`;

let Editor = styled('textarea')`
  background: var(--vapor-foreground);
  border-radius: 5px;
  height: calc(80vh - 40px);
  width: 100%;
  outline: none;
  border: none;
`;

let DigitalLogicCircuitWrapper = styled('div')`
  background: var(--vapor-background);
  border-bottom: 1px solid var(--vapor-accent-8);
`;

let VerificationWrapper = styled('div')`
  background: var(--vapor-background);
  border-bottom: 1px solid var(--vapor-accent-8);
`;

let BasisGateCircuitWrapper = styled('div')`
  background: var(--vapor-background);
`;

export default function Home() {
  return (
    <Wrapper>
      <LeftWrapper>
        <EditorWrapper>
          <Editor>

          </Editor>
        </EditorWrapper>
      </LeftWrapper>

      <RightWrapper>
        <DigitalLogicCircuitWrapper></DigitalLogicCircuitWrapper>

        <VerificationWrapper></VerificationWrapper>

        <BasisGateCircuitWrapper></BasisGateCircuitWrapper>
      </RightWrapper>
    </Wrapper>
  )
}
