import React, { useEffect, useState } from "react";
import { Modal } from "react-bootstrap";
import { withRouter } from "react-router-dom";
import { Button } from "../../components/Designs";

function ApiResponse() {
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false); 
  const handlePostRequest = () => {
    setLoading(true);

    const apiUrl = 'http://localhost:8000/get_feature';
    const data = {
      job_title: "L&D",
      company_name: "microsoft"
    };

    fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .then((data) => {
        setResponse(data);
        setIsModalOpen(true); 
        console.log(data);
      })
      .catch((error) => {
        console.error(error);
      })
      .finally(() => {
        setLoading(false);
      });
  };

  useEffect(() => {
    handlePostRequest();
  },[])

  const closeModal = () => {
    setIsModalOpen(false);
  };

  return (
    <div>
      <Button onClick={handlePostRequest} label={'Feature Spark'}></Button>

      {loading && <p>Loading...</p>}

      <Modal show={isModalOpen} onRequestClose={closeModal}  dialogClassName='hackathon-modal'>
        {response &&
        <div className="p-5" dangerouslySetInnerHTML={{ __html: response.features.html }} />
        }
        <Button onClick={closeModal} label={'Close'} className={'ml-5 mb-5'}></Button>
      </Modal>
      {/* {response && (
        <div>
          <div dangerouslySetInnerHTML={{ __html: response.features.html }} />
        </div>
      )} */}
    </div>
  );
}

export default withRouter(ApiResponse);
