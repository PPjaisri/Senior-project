import { useEffect, useState } from 'react';
import {
    Container, Row, Col, Tabs, Tab,
    InputGroup, FormControl, Form, Button
} from 'react-bootstrap';
import '../css/Search.css';

function Search() {
    return (
        <Container>
            <Row>
                <Col />
                <Col xs={6}>
                    <br />
                    <h4 className='text-center'>
                        <strong>
                            --- Thai news matcher ---
                        </strong>
                    </h4>
                    <hr />

                    <Tabs
                        defaultActiveKey="link"
                        transition={true}
                        className="mb-3"
                    >
                        <Tab eventKey="link" title="Link">
                            <label>Paste link here</label>
                            <p />
                            <InputGroup className="mb-3">
                                <FormControl
                                    placeholder="news link"
                                    aria-label="news link"
                                />
                                <Button variant="outline-secondary" id="link_submit">
                                    Search
                                </Button>
                            </InputGroup>
                        </Tab>
                        <Tab eventKey="content" title="Content">
                            <label>Paste news content here</label>
                            <p />
                            <InputGroup>
                                <FormControl
                                    as="textarea" aria-label="news content"
                                />
                                <Button variant="outline-secondary" id="content_submit">
                                    Search
                                </Button>
                            </InputGroup>
                        </Tab>
                        <Tab eventKey="image" title="Image">
                            <label>Upload file here</label>
                            <p />
                            <InputGroup className="mb-3">
                                <FormControl
                                    type="file"
                                    aria-label="news image"
                                />
                                <Button variant="outline-secondary" id="file_submit">
                                    Search
                                </Button>
                            </InputGroup>
                        </Tab>
                    </Tabs>
                </Col>
                <Col />
            </Row>
        </Container>
    )
}

export default Search;