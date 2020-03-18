
import React, { Component } from "react";
import { connect } from "react-redux";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import "./Roundup.css";

class RoundupContainer extends Component {
  render() {
    let num;
    this.props.size === "mobile" ? (num = 1) : (num = 2);

    return (
      <div className="main-container">
        <div className="headline roundup-headline">
          <span className="gold">Roundup</span>
        </div>

        <div className="roundup-container-text">
          <div className="subhead center roundup-subhead">
            News Roundup: latest updates on coding and web development
          </div>

          <p>